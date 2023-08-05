import os
import textwrap

from jinja2 import Template

from conan.tools._check_build_profile import check_using_build_profile
from conans.util.files import save


class BazelDeps(object):
    def __init__(self, conanfile):
        self._conanfile = conanfile
        check_using_build_profile(self._conanfile)

    def generate(self):
        local_repositories = []
        conandeps = self._conanfile.generators_folder

        for build_dependency in self._conanfile.dependencies.direct_build.values():
            content = self._get_build_dependency_buildfile_content(build_dependency)
            filename = self._save_dependency_buildfile(build_dependency, content, conandeps)

            local_repository = self._create_new_local_repository(build_dependency, filename)
            local_repositories.append(local_repository)

        for dependency in self._conanfile.dependencies.host.values():
            content = self._get_dependency_buildfile_content(dependency)
            if not content:
                continue
            filename = self._save_dependency_buildfile(dependency, content, conandeps)

            local_repository = self._create_new_local_repository(dependency, filename)
            local_repositories.append(local_repository)

        content = self._get_main_buildfile_content(local_repositories)
        self._save_main_buildfiles(content, conandeps)

    def _save_dependency_buildfile(self, dependency, buildfile_content, conandeps):
        filename = '{}/{}/BUILD.bazel'.format(conandeps, dependency.ref.name)
        save(filename, buildfile_content)
        return filename

    def _get_build_dependency_buildfile_content(self, dependency):
        filegroup = textwrap.dedent("""
            filegroup(
                name = "{}_binaries",
                data = glob(["**"]),
                visibility = ["//visibility:public"],
            )

        """).format(dependency.ref.name)

        return filegroup

    def _get_dependency_buildfile_content(self, dependency):
        template = textwrap.dedent("""
            load("@rules_cc//cc:defs.bzl", "cc_import", "cc_library")

            {% for lib in libs %}
            cc_import(
                name = "{{ lib }}_precompiled",
                {{ library_type }} = "{{ libdir }}/lib{{ lib }}.{{extension}}"
            )
            {% endfor %}

            cc_library(
                name = "{{ name }}",
                {% if headers %}
                hdrs = glob([{{ headers }}]),
                {% endif %}
                {% if includes %}
                includes = [{{ includes }}],
                {% endif %}
                {% if defines %}
                defines = [{{ defines }}],
                {% endif %}
                {% if linkopts %}
                linkopts = [{{ linkopts }}],
                {% endif %}
                visibility = ["//visibility:public"],
                {% if libs %}
                deps = [
                {% for lib in libs %}
                ":{{ lib }}_precompiled",
                {% endfor %}
                ],
                {% endif %}
            )

        """)

        cpp_info = dependency.cpp_info.aggregated_components()

        if not cpp_info.libs and not cpp_info.includedirs:
            return None

        headers = []
        includes = []

        def _relativize_path(p, base_path):
            # TODO: Very fragile, to test more
            if p.startswith(base_path):
                return p[len(base_path):].replace("\\", "/").lstrip("/")
            return p.replace("\\", "/").lstrip("/")

        # TODO: This only wokrs for package_folder, but not editable
        package_folder = dependency.package_folder
        for path in cpp_info.includedirs:
            headers.append('"{}/**"'.format(_relativize_path(path, package_folder)))
            includes.append('"{}"'.format(_relativize_path(path, package_folder)))

        headers = ', '.join(headers)
        includes = ', '.join(includes)

        defines = ('"{}"'.format(define.replace('"', "'"))
                   for define in cpp_info.defines)
        defines = ', '.join(defines)

        linkopts = []
        for linkopt in cpp_info.system_libs:
            linkopts.append('"-l{}"'.format(linkopt))
        linkopts = ', '.join(linkopts)


        lib_dir = 'lib'
        if len(cpp_info.libdirs) != 0:
            lib_dir = _relativize_path(cpp_info.libdirs[0], package_folder)

        shared_library = dependency.options.get_safe("shared") if dependency.options else False
        context = {
            "name": dependency.ref.name,
            "libs": cpp_info.libs,
            "libdir": lib_dir,
            "headers": headers,
            "includes": includes,
            "defines": defines,
            "linkopts": linkopts,
            "library_type": "shared_library" if shared_library else "static_library",
            "extension": "so" if shared_library else "a"
        }
        content = Template(template).render(**context)
        return content

    def _create_new_local_repository(self, dependency, dependency_buildfile_name):
        snippet = textwrap.dedent("""
            native.new_local_repository(
                name="{}",
                path="{}",
                build_file="{}",
            )
        """).format(
            dependency.ref.name,
            dependency.package_folder.replace("\\", "/"),
            dependency_buildfile_name.replace("\\", "/")
        )

        return snippet

    def _get_main_buildfile_content(self, local_repositories):
        template = textwrap.dedent("""
            def load_conan_dependencies():
                {}
        """)

        if local_repositories:
            function_content = "\n".join(local_repositories)
            function_content = '    '.join(line for line in function_content.splitlines(True))
        else:
            function_content = '    pass'

        content = template.format(function_content)

        return content

    def _save_main_buildfiles(self, content, conandeps):
        # A BUILD.bazel file must exist, even if it's empty, in order for Bazel
        # to detect it as a Bazel package and to allow to load the .bzl files
        save("{}/BUILD.bazel".format(conandeps), "")

        save("{}/dependencies.bzl".format(conandeps), content)
