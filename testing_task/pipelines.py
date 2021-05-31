import logging

from itemadapter import ItemAdapter


class StatusBuildPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('status') != None:
            if adapter['status'] == 0:
                adapter['status'] = 'Строится'
            elif adapter['status'] == 1:
                adapter['status'] = 'Сдан'
            elif adapter['status'] == 2:
                adapter['status'] = 'Проблемный'
        else:
            logging.error(
                f'При обработке новостройки с id {item["id_from_site"]} не '
                 'удалось найти статус постройки.'
            )

            
        return item


class ProcentSaleBuildPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['status'] == 'Строится':
            procent = adapter.get('sale_apartments')
            if procent != None:
                adapter['sale_apartments'] = int(procent * 100)
            else:
                logging.error(
                    f'При обработке новостройки с id {item["id_from_site"]} '
                        'не удалось найти распроданность квартир'
                )
        return item
