
from itemadapter import ItemAdapter


class StatusBuildPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('status'):
            if adapter['status'] == 0:
                adapter['status'] = 'Строится'
            if adapter['status'] == 1:
                adapter['status'] = 'Сдан'
            elif adapter['status'] == 2:
                adapter['status'] = 'Проблемный'
        return item
