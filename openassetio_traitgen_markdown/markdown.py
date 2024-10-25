import logging
import os
from openassetio_traitgen.generators import TraitGenerator
from openassetio_traitgen.datamodel import PackageDeclaration, TraitDeclaration, SpecificationDeclaration
from mdutils.mdutils import MdUtils

class MarkdownTraitGenerator(TraitGenerator):
    def generate(self,
        package_declaration: PackageDeclaration,
        globals_: dict,
        output_directory: str,
        creation_callback,
        logger: logging.Logger,):

        os.makedirs(output_directory, exist_ok=True)
        output = os.path.join(output_directory, f"{package_declaration.id}.md")
        mdFile = MdUtils(file_name=output,title=package_declaration.id)
        mdFile.new_paragraph(package_declaration.description)
        mdFile.new_paragraph("__TOC__")

        for kind in ('traits', 'specifications'):
            mdFile.new_header(level=1, title=kind.capitalize())
            namespaces = getattr(package_declaration, kind, None)
            if namespaces:
                for namespace in namespaces:
                    mdFile.new_header(level=2, title=namespace.id)
                    mdFile.new_paragraph(namespace.description)
                    mdFile.new_header(level=3, title='Members')
                    for member in namespace.members:
                        if isinstance(member, TraitDeclaration):
                            mdFile.new_header(level=4, title=member.name)
                            mdFile.new_paragraph(member.description)

                            if member.usage:
                                mdFile.new_header(level=5, title='Usage')
                                mdFile.new_list(member.usage)
                            
                            if member.properties:
                                mdFile.new_header(level=5, title='Properties')
                                for prop in member.properties:
                                    mdFile.new_header(level=6, title=prop.id)
                                    mdFile.new_paragraph("**Type**: " + prop.type.value)
                                    mdFile.new_paragraph("**Description:**\n" + prop.description)
                        elif isinstance(member, SpecificationDeclaration):
                            mdFile.new_header(level=4, title=member.id)
                            mdFile.new_paragraph(member.description)

                            if member.usage:
                                mdFile.new_header(level=5, title='Usage')
                                mdFile.new_list(member.usage)
                            
                            if member.trait_set:
                                mdFile.new_header(level=5, title='Trait Set')
                                for trait in member.trait_set:
                                    mdFile.new_header(level=6, title=trait.id)
                                    mdFile.new_paragraph("**Name**: " + trait.name)
                                    mdFile.new_paragraph("**Namespace**: " + trait.namespace)
                                    mdFile.new_paragraph("**Package**: " + trait.package)
                                    mdFile.new_paragraph("**Unique Name Parts**:")
                                    mdFile.new_list(trait.unique_name_parts)
                                

        mdFile.new_table_of_contents(table_title='Contents', depth=2, marker='__TOC__')
        mdFile.create_md_file()
        print(f"Markdown file created at {output}")