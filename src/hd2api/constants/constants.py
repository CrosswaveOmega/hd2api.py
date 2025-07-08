"""constant dictionaries."""

task_types = {
    2: "Gather",
    3: "Eradicate",
    4: "Objectives",
    7: "Extract",
    9: "Operations",
    11: "Liberation",
    12: "Defense",
    13: "Control",
    15: "Conquest",
}

value_types = {
    1: "faction",
    2: "hasCount",
    3: "goal",
    4: "enemyID",
    5: "itemID",
    6: "hasItem",
    7: "objective",
    8: "hasDifficulty",
    9: "difficulty",
    10: "unknown7",
    11: "hasPlanet",
    12: "planet",
}
faction_names = {
    0: "Anything",
    1: "Humans",
    2: "Terminids",
    3: "Automaton",
    4: "Illuminate",
    5: "ERR",
    15: "ERR",
}
faction_names_plural = {
    0: "Anything",
    1: "Humans",
    2: "the Terminids",
    3: "the Automatons",
    4: "the Illuminate",
    5: "ERR",
    15: "ERR",
}

region_size_enums = {0: "Settlement", 1: "Town", 2: "City", 3: "MegaCity"}

rewards = {897894480: 1, 3608481516: 2, 3481751602: 3}


samples = {
    3992382197: "Common",
    2985106497: "Rare",
}

items = {
    3992382197: "Common Sample",
    2985106497: "Rare Sample",
    3608481516: "Requisition Slips",
    897894480: "Medals",
    3481751602: "Super Credits",
}

enemies = {
    20706814: "Scout Strider",
    2664856027: "Shredder Tank",
    471929602: "Hulk",
    4276710272: "Devastator",
    878778730: "Trooper",
    3330362068: "Hunter",
    2058088313: "Warrior",
    2387277009: "Stalker",
    2651633799: "Charger",
    2514244534: "Bile Titan",
    1379865898: "Bile Spewer",
    4211847317: "Voteless",
}

stratagems = {
    1078307866: "ORBITAL GATLING BARRAGE",
    2928105092: "ORBITAL 120MM HE BARRAGE",
    2831720448: "ORBITAL AIRBURST STRIKE",
    4158531749: "ORBITAL 380MM HE BARRAGE",
    808823003: "ORBITAL WALKING BARRAGE",
    1520012896: "ORBITAL LASER",
    2197477188: "ORBITAL RAILCANNON STRIKE",
    3039399791: "ANTI-PERSONNEL MINEFIELD",
    336620886: "SUPPLY PACK",
    961518079: "Laser Cannon",
    1159284196: "Grenade Launcher",
    3111134131: "INCENDIARY MINES",
    4277455125: '"GUARD DOG" ROVER',
    2369837022: "BALLISTIC SHIELD BACKPACK",
    2138935687: "Arc Thrower",
    783152568: "ANTI-TANK MINES",
    1597673685: "Quasar Cannon",
    485637029: "SHIELD GENERATOR PACK",
    1228689284: "MACHINE GUN SENTRY",
    2446402932: "GATLING SENTRY",
    461790327: "MORTAR SENTRY",
    3791047893: '"GUARD DOG"',
    2616066963: "AUTOCANNON SENTRY",
    3467463065: "ROCKET SENTRY",
    3157053145: "EMS MORTAR SENTRY",
    2391781446: "ORBITAL PRECISION STRIKE",
    1134323464: "ORBITAL GAS STRIKE",
    3551336597: "ORBITAL EMS STRIKE",
    1363304012: "ORBITAL SMOKE STRIKE",
    70017975: "SHIELD GENERATOR RELAY",
    3827587060: "HMG EMPLACEMENT",
    1671728820: "TESLA TOWER",
    3857719901: "PATRIOT EXOSUIT",
    754365924: "EMANCIPATOR EXOSUIT",
    2025422424: "EAGLE STRAFING RUN",
    700547364: "EAGLE AIRSTRIKE",
    1220665708: "EAGLE CLUSTER BOMB",
    1427614189: "EAGLE NAPALM AIRSTRIKE",
    1062482104: "EAGLE SMOKE STRIKE",
    3863540692: "JUMP PACK",
    3723465233: "EAGLE 100MM ROCKET PODS",
    1982351727: "EAGLE 500KG BOMB",
    934703916: "Machine Gun",
    1978117092: "Stalwart",
    376960160: "Anti-Material Rifle",
    1207425221: "Expendable Anti-Tank",
    1594211884: "Recoilless Rifle",
    1944161163: "Flamethrower",
    841182351: "Autocannon",
    4038802832: "Heavy Machine Gun",
    3201417018: "Airburst Rocket Launcher",
    3212037062: "Commando",
    202236804: "Spear",
    295440526: "Railgun",
}

lines = {
    2: {
        "A": "Successfully extract with **#COUNT #ITEM_PRE#ITEM#ITEM_POST**#LOCATION_PRE#LOCATION#LOCATION_POST."
    },
    3: {
        "A": "Kill **#COUNT #ENEMY**#LOCATION_PRE#LOCATION#LOCATION_POST.",
        "IA": "Kill **#COUNT #ENEMY**#ITEM_PRE#ITEM#ITEM_POST#LOCATION_PRE#LOCATION#LOCATION_POST.",
    },
    7: {
        "R": "Extract from a successful #MTYPE against #RACE #DIFF_PRE#DIFF#DIFF_POST#COUNT_PRE#COUNT#COUNT_POST#MULTI#LOCATION_PRE#LOCATION#LOCATION_POST"
    },
    9: {
        "C": "Complete an Operation #DIFF_PRE#DIFF#DIFF_POST#COUNT_PRE#COUNT#COUNT_POST",
        "R": "Complete an Operation against #RACE #DIFF_PRE#DIFF#DIFF_POST#COUNT_PRE#COUNT#COUNT_POST",
    },
    11: {
        "L": "Liberate **#LOCATION**",
        "R": "Liberate **#COUNT** planets from **#RACE**",
    },
    12: {
        "C": "Defend against **#COUNT** attacks on any planet",
        "R": "Defend against **#COUNT** attacks from the **#RACE**",
    },
    13: {
        "L": "Hold **#LOCATION** when the order expires",
    },
    15: {
        "A": "Liberate more planets than are lost during the order duration",
        "R": "Liberate more planets than are lost to **#RACE** during the order duration",
    },
}
