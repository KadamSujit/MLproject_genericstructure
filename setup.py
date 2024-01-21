from setuptools import find_packages, setup
from typing import List


HYPEN_E_DOT="-e ."
# -e . is used to build the packages. when we give -e . then it automatically triggers setup.py
# But this -e . should not be there in requirements list because when we run requirements.txt and -e. occurs control goes to setup.py and this -e. is not a installable category of library for our project.
# Hence while reading requirements.txt we must remove -e. from the requirements list

#creating a function to get required libs
def get_requirements(file_path:str)->List[str]: #input file type is str and output will be in list form with list elements as strings
    '''
    This function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines() #reads line by line from requirement.txt
        requirements=[req.replace("\n","") for req in requirements] #list comprehension to remove \n that comes because of above used readlines() fun
        
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements


setup(
    name='mlproject_genericstructure', #setting up information for the project
    version='0.0.1',
    author='Sujit',
    author_email='sujitpkadam1991@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)
