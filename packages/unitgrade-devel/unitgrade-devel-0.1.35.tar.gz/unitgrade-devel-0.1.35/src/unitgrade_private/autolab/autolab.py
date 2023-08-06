"""
cd ~/Autolab && bundle exec rails s -p 8000 --binding=0.0.0.0

To remove my shitty image:
docker rmi tango_python_tue
"""
from zipfile import ZipFile
from os.path import basename
import os
import inspect
import shutil
from jinja2 import Environment, FileSystemLoader
import glob
from unitgrade.framework import Report
from unitgrade_private import docker_helpers
from importlib.machinery import SourceFileLoader

COURSES_BASE = "/home/tuhe/Autolab/courses/AutoPopulated"

CURDIR = os.path.dirname(__file__)
TEMPLATE_BASE = CURDIR + "/lab_template"


def jj(source, dest, data):
    if os.path.exists(dest) and os.path.samefile(source, dest):
        raise Exception()
    dir, f = os.path.split(source)
    file_loader = FileSystemLoader(dir)
    env = Environment(loader=file_loader)
    output = env.get_template(f).render(data)
    with open(dest, 'w') as f:
        f.write(output)
    return output


# def docker_build_image(tag='tango_python_tue'):
#     os.system(f"cd {CURDIR + '/../../../docker_images'}/docker_tango_python && docker build --tag {tag} .")
#     pass

def jj_handout(source, dest, data):
    out = jj(source, dest, data)
    shutil.copy(dest, dest+"-handout")
    return out


def zipFilesInDir(dirName, zipFileName, filter):
   with ZipFile(zipFileName, 'w') as zipObj:
       # Iterate over all the files in directory
       for folderName, subfolders, filenames in os.walk(dirName):
           for filename in filenames:
               if filter(filename):
                   # create complete filepath of file in directory
                   filePath = os.path.join(folderName, filename)
                   # Add file to zip
                   zipObj.write(filePath, basename(filePath))

def paths2report(base_path, report_file):
    mod = ".".join(os.path.relpath(report_file[:-3], base_path).split(os.sep))
    foo = SourceFileLoader(mod, report_file).load_module()
    # return foo.Report1
    # spec = importlib.util.spec_from_file_location(mod, report_file)
    # foo = importlib.util.module_from_spec(spec)
    for name, obj in inspect.getmembers(foo):
        if inspect.isclass(obj):
            # Last condition could be # and issubclass(obj, Report): but this is not safe when there are two
            # versions of unitgrade installed (git clone and pip installed package). So use this.
            if obj.__module__ == foo.__name__ and Report.__name__ in [c.__name__ for c in obj.mro()]:
                report = getattr(foo, name)
                return report
    return None

def run_relative(file, base):
    relative = os.path.relpath(file, base)
    mod = os.path.normpath(relative)[:-3].split(os.sep)
    os.system(f"cd {base} && python -m {'.'.join(mod)}")


def deploy_assignment(base_name, INSTRUCTOR_BASE, INSTRUCTOR_GRADE_FILE, STUDENT_BASE, STUDENT_GRADE_FILE,
                      output_tar=None,
                      COURSES_BASE=None,
                      autograde_image_tag='tango_python_tue'):

    assert os.path.isfile(INSTRUCTOR_GRADE_FILE)
    assert os.path.isfile(STUDENT_GRADE_FILE)
    assert os.path.isdir(INSTRUCTOR_BASE)
    assert os.path.isdir(STUDENT_BASE)

    deploy_directly = COURSES_BASE != None

    if COURSES_BASE == None:
        COURSES_BASE = os.getcwd() + "/tmp"
        if not os.path.exists(COURSES_BASE):
            os.mkdir(COURSES_BASE)

    LAB_DEST = os.path.join(COURSES_BASE, base_name)

    # STUDENT_HANDOUT_DIR = os.path.dirname(STUDENT_GRADE_FILE) #"/home/tuhe/Documents/unitgrade_private_v1/examples/example_simplest/students/programs"
    # INSTRUCTOR_GRADE_FILE = "/home/tuhe/Documents/unitgrade_private_v1/examples/example_simplest/instructor/programs/report5.py"
    # Make instructor token file.
    # Get the instructor result file.
    run_relative(INSTRUCTOR_GRADE_FILE, INSTRUCTOR_BASE)
    f = glob.glob(os.path.dirname(INSTRUCTOR_GRADE_FILE) + "/*.token")[0]
    from unitgrade_private import load_token
    res, _ = load_token(f)
    # with open(f, 'rb') as f:
    #     res = pickle.load(f)

    # Now we have the instructor token file. Let's get the student token file.
    total_ = res['total'][1]
    problems = []
    problems.append( dict(name='Unitgrade score', description='', max_score=total_, optional='false') )
    # for k, q in res['details'].items():
    #     problems.append(dict(name=q['title'], description='', max_score=q['possible'], optional='true'))
    # problems.append(dict(name="Autograding Total", description='The description (set in autolab.py)', max_score=total_, optional='false'))
    print(problems)

    sc = [('Total', res['total'][0])] + [(q['title'], q['obtained']) for k, q in res['details'].items()]
    ss = ", ".join( [f'"{t}": {s}' for t, s in sc] )
    scores = '{"scores": {' + ss + '}}'
    print(scores)

    # Quickly make student .token file to upload:
    # os.system(f"cd {os.path.dirname(STUDENT_HANDOUT_DIR)} && python -m programs.{os.path.basename(INSTRUCTOR_GRADE_FILE)[:-3]}")
    # os.system(f"cd {STUDENT_HANDOUT_DIR} && python {os.path.basename(INSTRUCTOR_GRADE_FILE)}")
    # handin_filename = os.path.basename(STUDENT_TOKEN_FILE)

    run_relative(STUDENT_GRADE_FILE, STUDENT_BASE)
    STUDENT_TOKEN_FILE = glob.glob(os.path.dirname(STUDENT_GRADE_FILE) + "/*.token")[0]
    handin_filename = os.path.basename( STUDENT_TOKEN_FILE)
    for _ in range(3):
        handin_filename = handin_filename[:handin_filename.rfind("_")]
    handin_filename += ".token"

    print("> Name of handin file", handin_filename)
    if os.path.exists(LAB_DEST):
        shutil.rmtree(LAB_DEST)
    os.mkdir(LAB_DEST)
    assert os.path.exists(TEMPLATE_BASE)

    # Make the handout directory.
    # Start in the src directory. You should make the handout files first.
    os.mkdir(LAB_DEST + "/src")

    INSTRUCTOR_REPORT_FILE = INSTRUCTOR_GRADE_FILE[:-9] + ".py"
    a = 234
    # /home/tuhe/Documents/unitgrade_private_v1/examples/example_simplest/instructor/programs/report5.py"
    data = {
            'base_name': base_name,
            # 'nice_name': base_name + "please",
            'display_name': paths2report(INSTRUCTOR_BASE, INSTRUCTOR_REPORT_FILE).title,
            'handin_filename': handin_filename,
            'autograde_image': autograde_image_tag,
            'src_files_to_handout': ['driver_python.py', 'student_sources.zip', handin_filename, os.path.basename(docker_helpers.__file__),
                                     os.path.basename(INSTRUCTOR_GRADE_FILE)], # Remove tname later; it is the upload.
            'instructor_grade_file': os.path.basename(INSTRUCTOR_GRADE_FILE),
            'grade_file_relative_destination': os.path.relpath(INSTRUCTOR_GRADE_FILE, INSTRUCTOR_BASE),
            'problems': problems,
            }

    # shutil.copyfile(TEMPLATE_BASE + "/hello.yml", f"{LAB_DEST}/{base_name}.yml")
    jj_handout(TEMPLATE_BASE + "/src/README", LAB_DEST + "/src/README", data)
    jj_handout(TEMPLATE_BASE + "/src/driver_python.py", LAB_DEST + "/src/driver_python.py", data)
    jj_handout(TEMPLATE_BASE + "/src/Makefile", LAB_DEST + "/src/Makefile",data)
    jj_handout(TEMPLATE_BASE + "/src/driver.sh", LAB_DEST + "/src/driver.sh",data)

    jj(TEMPLATE_BASE + "/Makefile", LAB_DEST + "/Makefile", data)
    jj(TEMPLATE_BASE + "/autograde-Makefile", LAB_DEST + "/autograde-Makefile",data=data)
    jj(TEMPLATE_BASE + "/hello.yml", f"{LAB_DEST}/{base_name}.yml", data=data)
    jj(TEMPLATE_BASE + "/hello.rb", f"{LAB_DEST}/{base_name}.rb", data=data)

    # Copy the student grade file to remove.
    shutil.copyfile(INSTRUCTOR_GRADE_FILE, f"{LAB_DEST}/src/{os.path.basename(INSTRUCTOR_GRADE_FILE)}")
    shutil.copyfile(STUDENT_TOKEN_FILE, f"{LAB_DEST}/src/{handin_filename}")
    shutil.make_archive(LAB_DEST + '/src/student_sources', 'zip', root_dir=STUDENT_BASE, base_dir=base_name)
    shutil.copyfile(docker_helpers.__file__, f"{LAB_DEST}/src/{os.path.basename(docker_helpers.__file__)}")
    os.mkdir(LAB_DEST +"/handin")
    os.mkdir(LAB_DEST +"/test-autograder") # Otherwise make clean will screw up.
    os.system(f"cd {LAB_DEST} && make && cd {CURDIR}")

    if deploy_directly:
        return None

    if output_tar is None:
        output_tar = os.getcwd() + "/" + base_name  + ".tar"

    shutil.make_archive(output_tar[:-4], 'tar', root_dir=COURSES_BASE, base_dir=base_name)
    return output_tar


if __name__ == "__main__":
    print("Deploying to", COURSES_BASE)
    docker_build_image()

    INSTRUCTOR_GRADE_FILE = "/home/tuhe/Documents/unitgrade_private_v1/examples/example_simplest/instructor/programs/report1_grade.py"
    INSTRUCTOR_BASE = "/home/tuhe/Documents/unitgrade_private_v1/examples/example_simplest/instructor"

    STUDENT_BASE = "/home/tuhe/Documents/unitgrade_private_v1/examples/example_simplest/students"
    STUDENT_GRADE_FILE = "/home/tuhe/Documents/unitgrade_private_v1/examples/example_simplest/students/programs/report1_grade.py"

    output_tar = deploy_assignment("hello4", INSTRUCTOR_BASE, INSTRUCTOR_GRADE_FILE, STUDENT_BASE, STUDENT_GRADE_FILE=STUDENT_GRADE_FILE)


def format_autolab_json(data, indent=None):
    import json

    stages = []
    pres = {
        "_presentation": "semantic",
        "stages": [], # "Build", "Test", "Timing"],
    }
    totals = {}
    for n, qs in data['details'].items():
        # print(n)
        title = qs['title']
        rs = {}
        for item, val in qs['items'].items():
            # print(item, val)
            item_name = item[1]
            pass_ = val['status'] == 'pass'
            d = {'passed': pass_}
            if not pass_:
                # Unfortunately, html is escaped in template, so linebreaks do not work.
                d['hint'] = val['stderr']
                # d['hint'] = "<br>".join( val['stderr'].strip().splitlines() )
            rs[item_name] = d
        totals[title] = qs['obtained']
        stages.append(title)
        pres[title] = rs
    summary_key = "Summary"
    stages.append(summary_key)
    pres['stages'] = stages
    pres[summary_key] = totals
    # rs = {
    #     "_presentation": "semantic",
    #     "stages": ["Build", "Test", "Timing"],
    #     "Test": {
    #         "Add Things": {
    #             "passed": True
    #         },
    #         "Return Values": {
    #             "passed": False,
    #             "hint": "You need to return 1"
    #         }
    #     },
    #     'scores': 234,
    #       'pass': True
    # }

    if indent is not None: # for debug.
        json_out = json.dumps(pres, indent=2)
    else:
        json_out = json.dumps(pres)
    print(json_out)
    scores = {"scores": {'Unitgrade score': data['total'][0] }} #, 'scoreboard': [data['total'][0]] }
    print( json.dumps(scores) )

    a = 234
    pass