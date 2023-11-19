id = Discord.User
if rarval < 4000:
        rarity = "Day-old"
        update_entry(id, 'Day-Old', readinfo(id)[5]+1)
    if 4000<= rarval < 7000:
        rarity = "Kids Sized"
        update_entry(id, 'Kids Sized', readinfo(id)[6]+1)
    if 7000<= rarval < 9000:
        rarity = "Standard"
        update_entry(id, 'Standard', readinfo(id)[7]+1)
    if 9000<= rarval < 9500:
        rarity = "Jumbo"
        update_entry(id, 'Jumbo', readinfo(id)[8]+1)
    if 9500<= rarval < 9700:
        rarity = "Bronze"
        update_entry(id, 'Bronze', readinfo(id)[9]+1)
    if 9700<= rarval < 9800:
        rarity = "Silver"
        update_entry(id, 'Silver', readinfo(id)[10]+1)
    if 9800<= rarval < 9900:
        rarity = "Gold"
        update_entry(id, 'Gold', readinfo(id)[11]+1)
    if 9900<= rarval < 9980:
        rarity = "Platinum"
        update_entry(id, 'Plaitinum', readinfo(id)[12]+1)
    if 9980<= rarval < 10000:
        rarity = "Donner"
        update_entry(id, 'Donner', readinfo(id)[13]+1)
    if rarval >=10000:
        rarity = "Bronze"
        update_entry(id, 'Bronze', readinfo(id)[9]+1)