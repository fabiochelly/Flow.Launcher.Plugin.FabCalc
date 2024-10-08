websearches = {
    "whois": {
        "name": "Whois Search",
        "search": "https://www.whois.com/whois/{q}",
        "link": "https://www.whois.com/whois/"
    },
    "tr": {
        "name": "Google Translate",
        "patterns": [
            ["^(en|es|fr|he|ja|ko|de|nl|pt) (en|es|fr|he|ja|ko|de|nl|pt) (.*)$", "https://translate.google.fr/?sl=$1&tl=$2&text=$3&op=translate"],
            ["^(en|es|fr|he|ja|ko|de|nl|pt) (.*)$", "https://translate.google.fr/?sl=auto&tl=$1&text=$2&op=translate"]
        ],
        "search": "https://translate.google.fr/?sl=auto&tl=fr&text={q}&op=translate",
        "link": "https://translate.google.fr/"
    },
    "dic": {
        "name": "Oxford Dictionary",
        "search": "https://www.oed.com/search/dictionary/?scope=Entries&q={q}",
        "link": "https://www.oed.com/?tl=true"
    }
}
