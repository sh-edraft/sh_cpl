from sh_edraft.publish.model.template import Template
from sh_edraft.publish.publisher import Publisher

if __name__ == '__main__':
    publisher = Publisher('./')
    templates = [
        Template('*', '../docs/init_template.txt')
    ]
    publisher.create(templates)
    publisher.publish()
