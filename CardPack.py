from constants import PACKS_STATS, TOTAL_CARDS
import numpy as np

class CardPack():
    def __init__(self, pack_rarity):
        pack_stats = PACKS_STATS[pack_rarity]
        self.card_quantity = pack_stats['cards_per_pack']
        self.rarities = list(pack_stats['odds'].keys())
        self.probabilities = np.array([pack_stats['odds'][rarity] for rarity in self.rarities])
        self.__album = {}

    def __populate_album(self):
        start_id = 0
        for rarity, count in TOTAL_CARDS.items():
            self.__album[rarity] = np.arange(start_id, start_id + count)
            start_id += count

    def open_pack(self, random_generator):
        self.__populate_album()
        rarites_open = random_generator.choice(self.rarities,
                                               size=self.card_quantity,
                                               p=self.probabilities,
                                               replace=True)
        cards_opened = []
        for rarity in rarites_open:
            cards_ids = int(random_generator.choice(self.__album[rarity]))
            cards_opened.append((rarity, cards_ids))
        return cards_opened
