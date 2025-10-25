import numpy as np
import pandas as pd
from collections import Counter
from CardPack import CardPack
from constants import DURATION_DAYS, PACKS_DAILY_DROP, TOTAL_CARDS

def simulate_single_player(seed=None):
    random_generator = np.random.default_rng(seed)
    owned = set()
    owned_by_rarity = {rarity: set() for rarity in TOTAL_CARDS}
    duplicates = 0
    daily_opens = []

    cards_opened_total = 0
    card_rarity_opened = Counter()
    packs_type_opened = Counter()

    for day in range(1, DURATION_DAYS + 1):
        for pack_rarity, per_day in PACKS_DAILY_DROP.items():
            card_pack = CardPack(pack_rarity)
            for i in range(per_day):
                packs_type_opened[pack_rarity] += 1
                for rarity, card_id in card_pack.open_pack(random_generator):
                    cards_opened_total += 1
                    card_rarity_opened[rarity] += 1
                    if card_id in owned:
                        duplicates += 1
                    else:
                        owned.add(card_id)
                        owned_by_rarity[rarity].add(card_id)

        opening = {
            'day': day,
            'unique_total': len(owned),
            'unique_common': len(owned_by_rarity['Common']),
            'unique_uncommon': len(owned_by_rarity['Uncommon']),
            'unique_rare': len(owned_by_rarity['Rare']),
            'completion_rate': len(owned) / sum(TOTAL_CARDS.values()),
            'duplicates_total': duplicates,
            'cards_total': cards_opened_total,
            'cards_common': card_rarity_opened['Common'],
            'cards_uncommon': card_rarity_opened['Uncommon'],
            'cards_rare': card_rarity_opened['Rare'],
            'packs_common': packs_type_opened['Common'],
            'packs_uncommon': packs_type_opened['Uncommon'],
            'packs_rare': packs_type_opened['Rare'],
        }
        daily_opens.append(opening)

    return pd.DataFrame(daily_opens)

def monte_carlo_sim(num_players=500, base_seed=13):
    all_players = []
    for player in range(num_players):
        seed = base_seed + player * 13
        single_player = simulate_single_player(seed=seed)
        single_player['player'] = player
        all_players.append(single_player)

    all_players_data = pd.concat(all_players, ignore_index=True)
    return all_players_data
