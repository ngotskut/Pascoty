import requests
import aiohttp
import asyncio
import time
from datetime import datetime
import re
import hashlib
import json

TELEGRAM_BOT_TOKEN = "8909596844:AAEO4vK4xgiIyl_WBPap_D4hds9jlNwSEIo"
TG_API = f"https://api.telegram.org/bot8909596844:AAEO4vK4xgiIyl_WBPap_D4hds9jlNwSEIo"
CHANNEL_URL = "https://t.me/"
DYNAMIC_GROUPS = ["-5125846224"]

FLAG_EMOJIS = {
    "🚩": "5294236848103643477", "🇦🇫": "5291937511591925566", "🇦🇽": "5294077418917616055", 
    "🇦🇱": "5294202819077756005", "🇩🇿": "5294048127240655242", "🇦🇸": "5291994273879709721", 
    "🇦🇩": "5294215205763434181", "🇦🇴": "5294516785482062829", "🇦🇮": "5292186323342350940", 
    "🇦🇬": "5294005972136647964", "🇦🇷": "5292208210495689627", "🇦🇲": "5291978717508164018", 
    "🇦🇼": "5294007002928798927", "🇦🇺": "5294444247779399477", "🇦🇹": "5291975174160145850", 
    "🇦🇿": "5294323533428579078", "🇧🇸": "5294031587321600012", "🇧🇭": "5294108398516720753", 
    "🇧🇩": "5291824687096027834", "🇧🇧": "5294526187165471742", "🇧🇾": "5294134426018536120", 
    "🇧🇪": "5291774466043435275", "🇧🇿": "5294171848068584842", "🇧🇯": "5293984969746566866", 
    "🇧🇹": "5294121983498277263", "🇧🇴": "5294201479047957700", "🇧🇼": "5294026179957772585", 
    "🇧🇷": "5291892229751723900", "🇧🇳": "5292098293692650297", "🇧🇬": "5294308947719640437", 
    "🇧🇫": "5294153164960848949", "🇧🇮": "5294051631933967760", "🇰🇭": "5294225191562400452", 
    "🇨🇲": "5291997306126626950", "🇨🇦": "5292290347450259214", "🇨🇻": "5292203503211535593", 
    "🇨🇫": "5294210571493724819", "🇹🇩": "5291780728105753403", "🇨🇱": "5294231037012888049", 
    "🇨🇳": "5294068833277990704", "🇨🇴": "5294010206974397371", "🇰🇲": "5294351381996521508", 
    "🇨🇬": "5294035229453865597", "🇨🇰": "5292098684534675100", "🇨🇷": "5292063805105263554", 
    "🇨🇮": "5293991322003200135", "🇭🇷": "5291999676948569127", "🇨🇺": "5291963947115631526", 
    "🇨🇾": "5294062721539526918", "🇨🇿": "5294242852467923382", "🇩🇰": "5294531860817268837", 
    "🇩🇯": "5294127214768468283", "🇩🇲": "5294485513825178032", "🇩🇴": "5294522197140857947", 
    "🇪🇨": "5292083733753517221", "🇪🇬": "5293992082212409502", "🇸🇻": "5294337307388695687", 
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿": "5294410107084365278", "🇬🇶": "5292170045416297012", "🇪🇷": "5291922054004625949", 
    "🇪🇪": "5291951143818123103", "🇪🇹": "5292245976143124155", "🇪🇺": "5291992809295861098", 
    "🇬🇮": "5292055799286224027", "🇬🇲": "5294399820637688352", "🇬🇱": "5292014752283774878", 
    "🇫🇮": "5294049961191690629", "🇫🇷": "5291817660529533837", "🇬🇦": "5294321325815389139", 
    "🇬🇪": "5294349389131697267", "🇩🇪": "5292013274815028523", "🇬🇭": "5294347396266873249", 
    "🇬🇷": "5291948395039054764", "🇬🇼": "5294409819321550432", "🇬🇹": "5294336633078831209", 
    "🇬🇳": "5291892096607739008", "🇬🇾": "5292062692708736193", "🇭🇹": "5292045130587462814", 
    "🇭🇳": "5291901034434682297", "🇭🇰": "5292166459118606932", "🇭🇺": "5294229581018975260", 
    "🇮🇸": "5294354358408859664", "🇮🇳": "5291933173674957761", "🇮🇷": "5294220170745630736", 
    "🇮🇶": "5294325010897327367", "🇮🇪": "5294471971793293647", "🇮🇲": "5294318478252070646", 
    "🇮🇱": "5294069056616289553", "🇮🇹": "5291826830284709120", "🇳🇬": "5294456308047563965", 
    "🇳🇺": "5294471336138134209", "🇳🇴": "5291761718580502030", "🇴🇲": "5291813666209946812", 
    "🇵🇰": "5291825606219029010", "🇵🇸": "5294289826525238172", "🇵🇦": "5291959935616178405", 
    "🇵🇬": "5291917995260533077", "🇵🇾": "5294525611639852679", "🇵🇭": "5291798075478661634", 
    "🇵🇪": "5292099427564018941", "🇵🇱": "5292190970496963836", "🇵🇹": "5294436555492973610", 
    "🇵🇷": "5292121516580820347", "🇶🇦": "5292166360334357676", "🇷🇴": "5294107724206856227", 
    "🇷🇺": "5294335323113807278", "🇷🇼": "5294191265615729158", "🇸🇲": "5292147350809106831", 
    "🇸🇹": "5292183188016222701", "🇸🇦": "5294163983983463099", "🏴󠁧󠁢󠁳󠁣󠁴󠁿": "5294434665707368018", 
    "🇸🇳": "5292087023698466689", "🇷🇸": "5294458584380230360", "🇸🇨": "5291891186074672309", 
    "🇸🇱": "5294494314213167952", "🇸🇬": "5294451304410663668", "🇸🇰": "5294538440707166931", 
    "🇸🇮": "5294279359689938006", "🇸🇧": "5294283890880433237", "🇸🇴": "5294058817414255960", 
    "🇿🇦": "5294325281480266304", "🇪🇸": "5294513087515216901", "🇱🇰": "5292102670264328257", 
    "🇸🇩": "5294177148058228060", "🇸🇷": "5294396668131692138", "🇸🇿": "5294312482477724867", 
    "🇸🇪": "5291737091238026321", "🇨🇭": "5291791748991835084", "🇸🇾": "5294013428199869487", 
    "🇹🇼": "5294095745543069603", "🇹🇯": "5294120269806328883", "🇹🇿": "5292146096678658977", 
    "🇹🇭": "5293994384314882755", "🇹🇬": "5294097669688415562", "🇯🇲": "5294505107465982830", 
    "🇯🇵": "5291799063321139445", "🇯🇪": "5291950280529697493", "🇯🇴": "5291988613112814801", 
    "🇰🇿": "5294227175837290463", "🇰🇪": "5292111852904416801", "🇰🇮": "5294538934628405146", 
    "🇰🇵": "5294193812531333564", "🇰🇷": "5294408281723262763", "🇰🇼": "5292066437920218075", 
    "🇰🇬": "5292091954320922577", "🇱🇦": "5291981530711746037", "🇱🇻": "5292236016113966127", 
    "🇱🇧": "5294193108156699621", "🇱🇸": "5292040693886247604", "🇱🇷": "5291793810576137439", 
    "🇱🇾": "5291858711826946840", "🇱🇮": "5292048742654957785", "🇱🇹": "5294343084119708700", 
    "🇱🇺": "5294423709245787718", "🇲🇰": "5294023611567332075", "🇲🇬": "5291991568050312348", 
    "🇲🇼": "5294241881805312589", "🇲🇾": "5291858351049696702", "🇲🇻": "5292004203844097218", 
    "🇲🇱": "5292086972158858331", "🇲🇹": "5294532213004588353", "🇲🇭": "5294180730060954484", 
    "🇲🇷": "5294429743674840973", "🇲🇺": "5294127824653797277", "🇲🇽": "5294535073452809778",
    "🇫🇲": "5291838156113470124", "🇲🇩": "5294158486425325375", "🇲🇨": "5294378161117614233", 
    "🇲🇳": "5294316532631883496", "🇲🇦": "5292108962391414885", "🇲🇿": "5294086708931874940", 
    "🇲🇲": "5294254478944393569", "🇳🇦": "5292021761670404922", "🇳🇷": "5294463274484521342", 
    "🇳🇵": "5294458756178924088", "🇳🇱": "5291917797692042265", "🇳🇿": "5294189019347833274", 
    "🇳🇮": "5294240825243358100", "🇳🇪": "5291809418487290691", "🇹🇴": "5294283689016973348", 
    "🇹🇹": "5294362935458548705", "🇹🇳": "5294484680601521871", "🇹🇷": "5293993400767367408", 
    "🇹🇲": "5294098958178603764", "🇹🇨": "5294320866253884749", "🇺🇸": "5294244076533600593", 
    "🇺🇬": "5294192317882716626", "🇦🇪": "5294314831824835370", "🇬🇧": "5293993521026453119", 
    "🇺🇦": "5294263837678131580", "🇻🇺": "5294448585696368047", "🇺🇿": "5294217645304864345", 
    "🇺🇾": "5291928449210932974", "🇻🇪": "5294476442854247878", "🇻🇳": "5294235963340379688", 
    "🇻🇮": "5294228039125718124", "🏴󠁧󠁢󠁷󠁬󠁳󠁿": "5294139949346476093", "🇾🇪": "5294058972033076492", 
    "🇿🇲": "5294100109229838880", "🇿🇼": "5294422158762592930", "🇮🇩": "5294378161117614233", 
    "🇹🇱": "5294001707234116044",
    "🇼🇸": "5294303252593001119",
    "🇳🇨": "5235605674020332176",
    "🇲🇪": "5294373621337179756",
    "🇽🇰": "5294134378773888806",
    "🇧🇦": "5294273286606175399",
    "🇻🇦": "5294358133685111262",
    "🇫🇴": "5296469342039327674",
    "🇸🇸": "5294310953469362786",
    "🇨🇩": "5294355333366435362",
    "🇵🇼": "5911283903187915549",
    "🇲🇶": "5911378005921370347"
}

APP_EMOJIS = {
    "WS": "5334998226636390258", "TG": "5330237710655306682", "FB": "5323261730283863478",
    "REDNOTE": "5334707727933390944", "SHP": "5373265917092316632", "IG": "5319160079465857105",
    "X": "5330337435500951363", "TK": "5327982530702359565", "DC": "5325612636467903082",
    "LINE": "5323608076446613036", "KAKAO": "5334933574493683027", "WECHAT": "5332524123610430820",
    "QQ": "5328064671951896068", "WEIBO": "5332823323917173335", "VK": "5334853932915114338",
    "THREADS": "5334592721594105691", "SNAP": "5330248916224983855", "TINDER": "5328029650788563621",
    "BUMBLE": "5323764984486837459", "GPT": "5359726582447487916", "APL": "5334955749409834455",
    "MS": "5370857634440170316", "GMAIL": "5373246052868571826", "GOOGLE": "5321244246705989720",
    "GITHUB": "5346181118884331907", "PLAY": "5373130604147654226", "APPSTORE": "5370722600668382252",
    "AMAZON": "5346056560537779652", "PAYPAL": "5364111181415996352", "LINKEDIN": "5346024520081751155",
    "VISA": "5364075889669718872", "MASTER": "5364036341610858181", "BTC": "5359584650958226302",
    "ETH": "5359321266383766546", "USDT": "5359320566304096699", "NFLX": "5318911503938634641",
    "YT": "5334807822146225472", "SPOTIFY": "5346074681004801565", "STEAM": "5373144051690258848",
    "PS": "5373306783706137993", "XBOX": "5373019729566908647", "TWC": "5334678011054669335",
    "DISNEY": "5332394707655869572"
}

country_map = {
    "1": ("United States", "🇺🇸", "US"),
    "1204": ("Canada", "🇨🇦", "CA"), "1226": ("Canada", "🇨🇦", "CA"), "1236": ("Canada", "🇨🇦", "CA"),
    "1249": ("Canada", "🇨🇦", "CA"), "1250": ("Canada", "🇨🇦", "CA"), "1289": ("Canada", "🇨🇦", "CA"),
    "1306": ("Canada", "🇨🇦", "CA"), "1343": ("Canada", "🇨🇦", "CA"), "1365": ("Canada", "🇨🇦", "CA"),
    "1403": ("Canada", "🇨🇦", "CA"), "1416": ("Canada", "🇨🇦", "CA"), "1418": ("Canada", "🇨🇦", "CA"),
    "1431": ("Canada", "🇨🇦", "CA"), "1437": ("Canada", "🇨🇦", "CA"), "1450": ("Canada", "🇨🇦", "CA"),
    "1506": ("Canada", "🇨🇦", "CA"), "1514": ("Canada", "🇨🇦", "CA"), "1519": ("Canada", "🇨🇦", "CA"),
    "1579": ("Canada", "🇨🇦", "CA"), "1581": ("Canada", "🇨🇦", "CA"), "1587": ("Canada", "🇨🇦", "CA"),
    "1604": ("Canada", "🇨🇦", "CA"), "1613": ("Canada", "🇨🇦", "CA"), "1639": ("Canada", "🇨🇦", "CA"),
    "1647": ("Canada", "🇨🇦", "CA"), "1705": ("Canada", "🇨🇦", "CA"), "1709": ("Canada", "🇨🇦", "CA"),
    "1742": ("Canada", "🇨🇦", "CA"), "1778": ("Canada", "🇨🇦", "CA"), "1780": ("Canada", "🇨🇦", "CA"),
    "1807": ("Canada", "🇨🇦", "CA"), "1819": ("Canada", "🇨🇦", "CA"), "1825": ("Canada", "🇨🇦", "CA"),
    "1867": ("Canada", "🇨🇦", "CA"), "1873": ("Canada", "🇨🇦", "CA"), "1902": ("Canada", "🇨🇦", "CA"),
    "1905": ("Canada", "🇨🇦", "CA"),
    "1787": ("Puerto Rico", "🇵🇷", "PR"), "1939": ("Puerto Rico", "🇵🇷", "PR"),
    "1876": ("Jamaica", "🇯🇲", "JM"), "1242": ("Bahamas", "🇧🇸", "BS"),
    "1246": ("Barbados", "🇧🇧", "BB"),
    "20": ("Egypt", "🇪🇬", "EG"), "211": ("South Sudan", "🇸🇸", "SS"),
    "212": ("Morocco", "🇲🇦", "MA"), "213": ("Algeria", "🇩🇿", "DZ"),
    "216": ("Tunisia", "🇹🇳", "TN"), "218": ("Libya", "🇱🇾", "LY"),
    "220": ("Gambia", "🇬🇲", "GM"), "221": ("Senegal", "🇸🇳", "SN"),
    "222": ("Mauritania", "🇲🇷", "MR"), "223": ("Mali", "🇲🇱", "ML"),
    "224": ("Guinea", "🇬🇳", "GN"), "225": ("Ivory Coast", "🇨🇮", "CI"),
    "226": ("Burkina Faso", "🇧🇫", "BF"), "227": ("Niger", "🇳🇪", "NE"),
    "228": ("Togo", "🇹🇬", "TG"), "229": ("Benin", "🇧🇯", "BJ"),
    "230": ("Mauritius", "🇲🇺", "MU"), "231": ("Liberia", "🇱🇷", "LR"),
    "232": ("Sierra Leone", "🇸🇱", "SL"), "233": ("Ghana", "🇬🇭", "GH"),
    "234": ("Nigeria", "🇳🇬", "NG"), "235": ("Chad", "🇹🇩", "TD"),
    "236": ("Central African Rep.", "🇨🇫", "CF"), "237": ("Cameroon", "🇨🇲", "CM"),
    "238": ("Cape Verde", "🇨🇻", "CV"), "239": ("Sao Tome & Principe", "🇸🇹", "ST"),
    "240": ("Equatorial Guinea", "🇬🇶", "GQ"), "241": ("Gabon", "🇬🇦", "GA"),
    "242": ("Congo", "🇨🇬", "CG"), "243": ("DR Congo", "🇨🇩", "CD"),
    "244": ("Angola", "🇦🇴", "AO"), "245": ("Guinea-Bissau", "🇬🇼", "GW"),
    "246": ("Diego Garcia", "🇮🇴", "IO"), "247": ("Ascension Island", "🇦🇨", "AC"),
    "248": ("Seychelles", "🇸🇨", "SC"), "249": ("Sudan", "🇸🇩", "SD"),
    "250": ("Rwanda", "🇷🇼", "RW"), "251": ("Ethiopia", "🇪🇹", "ET"),
    "252": ("Somalia", "🇸🇴", "SO"), "253": ("Djibouti", "🇩🇯", "DJ"),
    "254": ("Kenya", "🇰🇪", "KE"), "255": ("Tanzania", "🇹🇿", "TZ"),
    "256": ("Uganda", "🇺🇬", "UG"), "257": ("Burundi", "🇧🇮", "BI"),
    "258": ("Mozambique", "🇲🇿", "MZ"), "260": ("Zambia", "🇿🇲", "ZM"),
    "261": ("Madagascar", "🇲🇬", "MG"), "262": ("Reunion", "🇷🇪", "RE"),
    "263": ("Zimbabwe", "🇿🇼", "ZW"), "264": ("Namibia", "🇳🇦", "NA"),
    "265": ("Malawi", "🇲🇼", "MW"), "266": ("Lesotho", "🇱🇸", "LS"),
    "267": ("Botswana", "🇧🇼", "BW"), "268": ("Eswatini", "🇸🇿", "SZ"),
    "269": ("Comoros", "🇰🇲", "KM"), "27": ("South Africa", "🇿🇦", "ZA"),
    "290": ("Saint Helena", "🇸🇭", "SH"), "291": ("Eritrea", "🇪🇷", "ER"),
    "297": ("Aruba", "🇦🇼", "AW"), "298": ("Faroe Islands", "🇫🇴", "FO"),
    "299": ("Greenland", "🇬🇱", "GL"),
    "30": ("Greece", "🇬🇷", "GR"), "31": ("Netherlands", "🇳🇱", "NL"),
    "32": ("Belgium", "🇧🇪", "BE"), "33": ("France", "🇫🇷", "FR"),
    "34": ("Spain", "🇪🇸", "ES"), "350": ("Gibraltar", "🇬🇮", "GI"),
    "351": ("Portugal", "🇵🇹", "PT"), "352": ("Luxembourg", "🇱🇺", "LU"),
    "353": ("Ireland", "🇮🇪", "IE"), "354": ("Iceland", "🇮🇸", "IS"),
    "355": ("Albania", "🇦🇱", "AL"), "356": ("Malta", "🇲🇹", "MT"),
    "357": ("Cyprus", "🇨🇾", "CY"), "358": ("Finland", "🇫🇮", "FI"),
    "359": ("Bulgaria", "🇧🇬", "BG"), "36": ("Hungary", "🇭🇺", "HU"),
    "370": ("Lithuania", "🇱🇹", "LT"), "371": ("Latvia", "🇱🇻", "LV"),
    "372": ("Estonia", "🇪🇪", "EE"), "373": ("Moldova", "🇲🇩", "MD"),
    "374": ("Armenia", "🇦🇲", "AM"), "375": ("Belarus", "🇧🇾", "BY"),
    "376": ("Andorra", "🇦🇩", "AD"), "377": ("Monaco", "🇲🇨", "MC"),
    "378": ("San Marino", "🇸🇲", "SM"), "379": ("Vatican City", "🇻🇦", "VA"),
    "380": ("Ukraine", "🇺🇦", "UA"), "381": ("Serbia", "🇷🇸", "RS"),
    "382": ("Montenegro", "🇲🇪", "ME"), "383": ("Kosovo", "🇽🇰", "XK"),
    "385": ("Croatia", "🇭🇷", "HR"), "386": ("Slovenia", "🇸🇮", "SI"),
    "387": ("Bosnia & Herzegovina", "🇧🇦", "BA"), "389": ("North Macedonia", "🇲🇰", "MK"),
    "39": ("Italy", "🇮🇹", "IT"), "40": ("Romania", "🇷🇴", "RO"),
    "41": ("Switzerland", "🇨🇭", "CH"), "420": ("Czechia", "🇨🇿", "CZ"),
    "421": ("Slovakia", "🇸🇰", "SK"), "423": ("Liechtenstein", "🇱🇮", "LI"),
    "43": ("Austria", "🇦🇹", "AT"), "44": ("United Kingdom", "🇬🇧", "GB"),
    "45": ("Denmark", "🇩🇰", "DK"), "46": ("Sweden", "🇸🇪", "SE"),
    "47": ("Norway", "🇳🇴", "NO"), "48": ("Poland", "🇵🇱", "PL"),
    "49": ("Germany", "🇩🇪", "DE"),
    "500": ("Falkland Islands", "🇫🇰", "FK"), "501": ("Belize", "🇧🇿", "BZ"),
    "502": ("Guatemala", "🇬🇹", "GT"), "503": ("El Salvador", "🇸🇻", "SV"),
    "504": ("Honduras", "🇭🇳", "HN"), "505": ("Nicaragua", "🇳🇮", "NI"),
    "506": ("Costa Rica", "🇨🇷", "CR"), "507": ("Panama", "🇵🇦", "PA"),
    "508": ("St. Pierre & Miquelon", "🇵🇲", "PM"), "509": ("Haiti", "🇭🇹", "HT"),
    "51": ("Peru", "🇵🇪", "PE"), "52": ("Mexico", "🇲🇽", "MX"),
    "53": ("Cuba", "🇨🇺", "CU"), "54": ("Argentina", "🇦🇷", "AR"),
    "55": ("Brazil", "🇧🇷", "BR"), "56": ("Chile", "🇨🇱", "CL"),
    "57": ("Colombia", "🇨🇴", "CO"), "58": ("Venezuela", "🇻🇪", "VE"),
    "590": ("Guadeloupe", "🇬🇵", "GP"), "591": ("Bolivia", "🇧🇴", "BO"),
    "592": ("Guyana", "🇬🇾", "GY"), "593": ("Ecuador", "🇪🇨", "EC"),
    "594": ("French Guiana", "🇬🇫", "GF"), "595": ("Paraguay", "🇵🇾", "PY"),
    "596": ("Martinique", "🇲🇶", "MQ"), "597": ("Suriname", "🇸🇷", "SR"),
    "598": ("Uruguay", "🇺🇾", "UY"), "599": ("Curacao", "🇨🇼", "CW"),
    "60": ("Malaysia", "🇲🇾", "MY"), "61": ("Australia", "🇦🇺", "AU"),
    "62": ("Indonesia", "🇮🇩", "ID"), "63": ("Philippines", "🇵🇭", "PH"),
    "64": ("New Zealand", "🇳🇿", "NZ"), "65": ("Singapore", "🇸🇬", "SG"),
    "66": ("Thailand", "🇹🇭", "TH"), "670": ("Timor-Leste", "🇹🇱", "TL"),
    "672": ("Antarctica", "🇦🇶", "AQ"), "673": ("Brunei", "🇧🇳", "BN"),
    "674": ("Nauru", "🇳🇷", "NR"), "675": ("Papua New Guinea", "🇵🇬", "PG"),
    "676": ("Tonga", "🇹🇴", "TO"), "677": ("Solomon Islands", "🇸🇧", "SB"),
    "678": ("Vanuatu", "🇻🇺", "VU"), "679": ("Fiji", "🇫🇯", "FJ"),
    "680": ("Palau", "🇵🇼", "PW"), "681": ("Wallis & Futuna", "🇼🇫", "WF"),
    "682": ("Cook Islands", "🇨🇰", "CK"), "683": ("Niue", "🇳🇺", "NU"),
    "685": ("Samoa", "🇼🇸", "WS"), "686": ("Kiribati", "🇰🇮", "KI"),
    "687": ("New Caledonia", "🇳🇨", "NC"), "688": ("Tuvalu", "🇹🇻", "TV"),
    "689": ("French Polynesia", "🇵🇫", "PF"), "690": ("Tokelau", "🇹🇰", "TK"),
    "691": ("Micronesia", "🇫🇲", "FM"), "692": ("Marshall Islands", "🇲🇭", "MH"),
    "7": ("Russia", "🇷🇺", "RU"), "76": ("Kazakhstan", "🇰🇿", "KZ"), "77": ("Kazakhstan", "🇰🇿", "KZ"),
    "81": ("Japan", "🇯🇵", "JP"), "82": ("South Korea", "🇰🇷", "KR"),
    "84": ("Vietnam", "🇻🇳", "VN"), "850": ("North Korea", "🇰🇵", "KP"),
    "852": ("Hong Kong", "🇭🇰", "HK"), "853": ("Macau", "🇲🇴", "MO"),
    "855": ("Cambodia", "🇰🇭", "KH"), "856": ("Laos", "🇱🇦", "LA"),
    "86": ("China", "🇨🇳", "CN"), "880": ("Bangladesh", "🇧🇩", "BD"),
    "886": ("Taiwan", "🇹🇼", "TW"),
    "90": ("Turkey", "🇹🇷", "TR"), "91": ("India", "🇮🇳", "IN"),
    "92": ("Pakistan", "🇵🇰", "PK"), "93": ("Afghanistan", "🇦🇫", "AF"),
    "94": ("Sri Lanka", "🇱🇰", "LK"), "95": ("Myanmar", "🇲🇲", "MM"),
    "960": ("Maldives", "🇲🇻", "MV"), "961": ("Lebanon", "🇱🇧", "LB"),
    "962": ("Jordan", "🇯🇴", "JO"), "963": ("Syria", "🇸🇾", "SY"),
    "964": ("Iraq", "🇮🇶", "IQ"), "965": ("Kuwait", "🇰🇼", "KW"),
    "966": ("Saudi Arabia", "🇸🇦", "SA"), "967": ("Yemen", "🇾🇪", "YE"),
    "968": ("Oman", "🇴🇲", "OM"), "970": ("Palestine", "🇵🇸", "PS"),
    "971": ("UAE", "🇦🇪", "AE"), "972": ("Israel", "🇮🇱", "IL"),
    "973": ("Bahrain", "🇧🇭", "BH"), "974": ("Qatar", "🇶🇦", "QA"),
    "975": ("Bhutan", "🇧🇹", "BT"), "976": ("Mongolia", "🇲🇳", "MN"),
    "977": ("Nepal", "🇳🇵", "NP"), "98": ("Iran", "🇮🇷", "IR"),
    "992": ("Tajikistan", "🇹🇯", "TJ"), "993": ("Turkmenistan", "🇹🇲", "TM"),
    "994": ("Azerbaijan", "🇦🇿", "AZ"), "995": ("Georgia", "🇬🇪", "GE"),
    "996": ("Kyrgyzstan", "🇰🇬", "KG"), "998": ("Uzbekistan", "🇺🇿", "UZ")
}

tg_session = requests.Session()
sent_cache = set()

def escape_html(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def format_phone(phone):
    ring = '<tg-emoji emoji-id="5462882007451185227">💫</tg-emoji>'
    return phone[:4] + ring + phone[-4:] if len(phone) >= 8 else phone

def get_country(phone: str):
    clean = phone.lstrip('+')
    for code in sorted(country_map.keys(), key=len, reverse=True):
        if clean.startswith(code):
            name, flag, iso = country_map[code]
            if flag in FLAG_EMOJIS:
                flag = f'<tg-emoji emoji-id="{FLAG_EMOJIS[flag]}">{flag}</tg-emoji>'
            return name, flag, iso
    return "Unknown", '<tg-emoji emoji-id="5287292843763713628">🌍</tg-emoji>', "UN"

def extract_service(text: str, cli: str = "") -> str:
    lower = text.lower()
    cli_lower = cli.lower()
    
    if "imo" in lower:
        return None
        
    known_apps = {
        "whatsapp": ("WS", "💬"), "wa": ("WS", "💬"),
        "telegram": ("TG", "✈️"), "tg": ("TG", "✈️"),
        "xiaohongshu": ("REDNOTE", "📕"), "rednote": ("REDNOTE", "📕"),
        "facebook": ("FB", "📘"), "fb": ("FB", "📘"),
        "instagram": ("IG", "📸"), "ig": ("IG", "📸"), 
        "twitter": ("X", "🐦"), "x": ("X", "🐦"),
        "tiktok": ("TK", "🎵"), "discord": ("DC", "👾"),
        "line": ("LINE", "💬"), "kakao": ("KAKAO", "💛"), "kakaotalk": ("KAKAO", "💛"),
        "wechat": ("WECHAT", "💬"), "qq": ("QQ", "🐧"), "weibo": ("WEIBO", "👁"),
        "vk": ("VK", "🟦"), "threads": ("THREADS", "🧵"), "snapchat": ("SNAP", "👻"), 
        "snap": ("SNAP", "👻"),
        "tinder": ("TINDER", "🔥"), "bumble": ("BUMBLE", "🐝"),
        "shopee": ("SHP", "🛍"), "spaylater": ("SHP", "🛍"), "shopeepay": ("SHP", "🛍"),
        "linkedin": ("LINKEDIN", "💼"), "paypal": ("PAYPAL", "💸"), "amazon": ("AMAZON", "🛒"),
        "visa": ("VISA", "💳"), "mastercard": ("MASTER", "💳"),
        "bitcoin": ("BTC", "₿"), "btc": ("BTC", "₿"),
        "ethereum": ("ETH", "Ξ"), "eth": ("ETH", "Ξ"),
        "usdt": ("USDT", "💵"), "tether": ("USDT", "💵"),
        "twitch": ("TWC", "🎮"), "steam": ("STEAM", "💨"),
        "playstation": ("PS", "🎮"), "psn": ("PS", "🎮"), "xbox": ("XBOX", "❎"),
        "netflix": ("NFLX", "🎬"), "spotify": ("SPOTIFY", "🎧"), "youtube": ("YT", "▶️"), 
        "disney": ("DISNEY", "🏰"),
        "apple": ("APL", "🍎"), "microsoft": ("MS", "🪟"),
        "gmail": ("GMAIL", "📧"), "google": ("GOOGLE", "🔍"),
        "chatgpt": ("GPT", "🤖"), "openai": ("GPT", "🤖"), "gpt": ("GPT", "🤖"),
        "github": ("GITHUB", "🐙"), "playstore": ("PLAY", "▶️"), "google play": ("PLAY", "▶️"),
        "appstore": ("APPSTORE", "🍏"), "app store": ("APPSTORE", "🍏")
    }

    for keyword, (app_code, icon) in known_apps.items():
        if re.search(rf'\b{keyword}\b', lower) or re.search(rf'\b{keyword}\b', cli_lower):
            if app_code in APP_EMOJIS:
                return f'<tg-emoji emoji-id="{APP_EMOJIS[app_code]}">{icon}</tg-emoji>'
            return f"#{app_code}"

    hash_services = {
        "dbs bank": "#DBS", "dbs": "#DBS", "air france": "#AF", "airfrance": "#AF",
        "twverify": "#TWV", "indrive": "#IND", "airasia": "#AA", "grab": "#GRB",
        "lazada": "#LZD", "skrill": "#SKR", "fedbnk": "#FED", "iatsms": "#IAT",
        "bybit": "#BYB", "infobank": "#IB", "estateguru": "#EG", "dls": "#DLS",
        "vonagevf": "#VON", "vonage": "#VON", "klm": "#KLM"
    }
    for keyword, code in hash_services.items():
        if re.search(rf'\b{keyword}\b', lower) or re.search(rf'\b{keyword}\b', cli_lower):
            return code

    cli_alpha = re.sub(r'[^a-zA-Z]', '', cli)
    if len(cli_alpha) >= 2:
        return f"#{cli_alpha[:2].upper()}"
    elif len(cli_alpha) == 1:
        return f"#{cli_alpha.upper()}"

    fallback_patterns = [
        r'(?i)\[([a-zA-Z]{2,})\]',
        r'(?i)(?:your|from)\s+([a-zA-Z]{2,})',
        r'(?i)([a-zA-Z]{2,})\s+(?:code|otp|verification|password|pin)',
        r'^([A-Z][a-zA-Z]{1,})\b'
    ]
    
    ignore_words = {
        "your", "you", "the", "a", "an", "this", "that", "it", "my", "our", "we", "us",
        "is", "are", "was", "for", "from", "to", "of", "in", "on", "at", "with", "by", "and", "or",
        "code", "otp", "pin", "password", "passcode", "verification", "verify", "verifikasi", 
        "authentication", "auth", "login", "log", "register", "registration", "signup", "sign",
        "please", "do", "not", "use", "share", "give", "provide", "anyone", "someone", "staff", "admin",
        "never", "warning", "secret", "valid", "expires", "minute", "minutes", "time", "one",
        "account", "akun", "security", "access", "confirmation", "confirm", "number", "mobile", 
        "phone", "sms", "message", "text", "system", "alert", "info",
        "dear", "hi", "hello", "new", "reset", "change", "update", "recovery", "app", "application"
    }

    for pattern in fallback_patterns:
        match = re.search(pattern, text)
        if match:
            extracted = match.group(1)
            if extracted.lower() not in ignore_words:
                return f"#{extracted[:2].upper()}"

    return "#UN"

def extract_otp(text: str) -> str:
    match = re.search(r'(?<!\d)(\d{3}[-\s]?\d{3,4}|\d{4,8})(?!\d)', text)
    if match:
        return re.sub(r'[- ]', '', match.group(1))
    return "N/A"

def tg_post(endpoint: str, payload: dict):
    try:
        resp = tg_session.post(f"{TG_API}/{endpoint}", json=payload, timeout=20)
        return resp.json()
    except:
        return None

def tg_send_text(chat_id, msg: str, reply_markup=None):
    payload = {"chat_id": chat_id, "text": msg, "parse_mode": "HTML", "disable_web_page_preview": True}
    if reply_markup: payload["reply_markup"] = reply_markup
    return tg_post("sendMessage", payload)

async def scan_pscall_panel(panel_config):
    results = []
    api_url = panel_config["API_URL"]
    api_key = panel_config["TOKEN"]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01"
    }
    
    try:
        params = {
            "key": api_key, 
            "start": "0",
            "length": "100"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params, headers=headers, timeout=10) as r:
                if r.status != 200:
                    return []
                r_text = await r.text()
        
        data = json.loads(r_text)
        
        if data.get("result") != "success":
            return []
            
        for item in data.get("data", []):
            if isinstance(item, dict):
                phone = str(item.get("num", item.get("number", item.get("destination", "")))).strip()
                full_msg = str(item.get("message", item.get("sms", ""))).strip().replace('\n', ' ').replace('  ', ' ')
                date_str = str(item.get("dt", item.get("date", item.get("time", "")))).strip()
                cli = str(item.get("cli", item.get("sender", "")))
            elif isinstance(item, list) and len(item) >= 4:
                date_str = str(item[0])
                phone = str(item[2])
                cli = str(item[3])
                full_msg = str(item[4] if len(item) > 4 else item[3]).replace('\n', ' ').replace('  ', ' ')
            else:
                continue

            if not phone or not full_msg: continue
            
            app = extract_service(full_msg, cli)
            if not app or "imo" in full_msg.lower(): continue
            otp = extract_otp(full_msg)
            if otp == "N/A": continue
            
            sms_hash = hashlib.md5(f"{phone}{full_msg}".encode('utf-8')).hexdigest()[:8]
            try:
                ts = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            except:
                ts = datetime.now()
                
            name, flag, iso = get_country(phone)
            results.append({
                "phone": phone, "app": app, "full_msg": full_msg, 
                "otp": otp, "hash": sms_hash, "timestamp": ts, 
                "country": name, "flag": flag, "iso": iso
            })
            
    except:
        pass
        
    return results

async def panel_worker():
    config = {
        "API_URL": "http://pscall.net/restapi/smsreport",
        "TOKEN": "SFdUSD1SS3d2ioiJRlI="
    }
    
    while True:
        try:
            entries = await scan_pscall_panel(config)
            
            for entry in reversed(entries):
                unique_id = f"{entry['phone']}:{entry['otp']}:{entry['hash']}"
                
                if unique_id not in sent_cache:
                    sent_cache.add(unique_id)
                    if len(sent_cache) > 10000:
                        sent_cache.clear()
                        
                    ENV_EMOJI  = '<tg-emoji emoji-id="5454113432284446338">✉️</tg-emoji>'
                    b_text = f"{entry['flag']} {entry['iso']} {entry['app']} {format_phone(entry['phone'])} {ENV_EMOJI}"
                    
                    rmarkup = {
                        "inline_keyboard": [
                            [
                                {
                                    "text": f"{entry['otp']}", 
                                    "copy_text": {"text": entry['otp']},
                                    "icon_custom_emoji_id": "5215677360774324968",
                                    "style": "success"
                                }
                            ],
                            [
                                {
                                    "text": "Channel", 
                                    "url": CHANNEL_URL,
                                    "icon_custom_emoji_id": "6246698201642960198",
                                    "style": "primary"
                                },
                                {
                                    "text": "Number", 
                                    "url": "https://t.me/ngotskuy",
                                    "icon_custom_emoji_id": "5861820727639937460",
                                    "style": "primary"
                                }
                            ]
                        ]
                    }
                    
                    for g_chat_id in DYNAMIC_GROUPS:
                        tg_send_text(g_chat_id, b_text, rmarkup)
                        
        except:
            pass
            
        await asyncio.sleep(2)

async def main():
    await panel_worker()

if __name__ == "__main__":
    asyncio.run(main())