from setuptools import setup
from vault_shell import __version__

setup(
    name='vault-shell',
    version=__version__,
    description="An interactive Command Line Shell for Openstack CLI",
    long_description="Interactive command shell for Openstack",
    url="https://github.com/bdastur/vault-shell",
    author="Behzad Dastur",
    author_email="bdastur@gmail.com",
    license="MIT",
    packages=["vault_shell"],
    classifier=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'License :: Apache Software License',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],
    keywords="openstack cli autocomplete syntax",
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'vault-shell = vault_shell.main:run'
        ]
    },
    install_requires=['prompt-toolkit',
                      'PyYAML',
                      'Pygments']
)
