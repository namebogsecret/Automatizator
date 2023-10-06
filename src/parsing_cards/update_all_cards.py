#/src/parsing_cards/update_all_cards.py
from logging import getLogger
from src.database.add_card_to_sql import add_card_to_sql
from src.database.is_modified import was_not_modified
from src.database.update_card_in_sql import update_card_in_sql
from src.parsing_cards.get_all_cards import CardGetter
from src.database.compare_to_database import compare_to_database
from src.parsing_cards.processor_3 import CardProcessor3
from src.log_scripts.set_logger import set_logger

# logger setup5
logger = getLogger(__name__)
logger = set_logger(logger)
# Получение всех карточек


class CardUpdater:
    def __init__(self, driver, sql):
        self.driver = driver
        self.sql = sql
        self.cardgetter = CardGetter(driver)

    def update_all_cards(self):
        cards = self.cardgetter.get_all_cards()
        if cards != []:
            cards_parsed = []
            logger.info('Number of cards: %s', len(cards))
            for i in range(0, len(cards)):
                card = CardProcessor3(cards[i])
                card = card.process_3()
                if card is not None:
                    if card['url'] is None:
                        continue
                    cards_parsed.append(card)
                    logger.debug("Карточка (%s) %s не нулевая", i, card['id'])
                    if compare_to_database(card, self.sql) == False:
                            add_card_to_sql(self.sql, card)
                            logger.info("Карточка (%s) %s добавлена в базу данных", i, card['id'])
                    elif was_not_modified(card, self.sql) == True and card['modified'] is not None:
                            update_card_in_sql(self.sql, card)
                            logger.info("Карточка (%s) %s обновлена в базе данных", i, card['id'])
                    else:
                            logger.info("Карточка (%s) %s уже есть в базе данных и не изменена", i, card['id'])
                else:
                    logger.info("Карточка (%s) нулевая", i)
            self.sql.commit()
            return cards_parsed
        else:
            logger.info("Карточек не найдено")
            return []