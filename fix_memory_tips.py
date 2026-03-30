# -*- coding: utf-8 -*-
"""
修复记忆提示 - 用英文思维记忆法替换简单的"记住xxx"和"xxx=yyy"格式
"""
import re
import glob

# 英文思维记忆提示字典
MEMORY_TIPS = {
    # 衣物类
    "shoes": "shoe=鞋，-s=复数，穿在脚上的保护用品",
    "coat": "coat=外套，像涂层一样裹住身体",
    "pillow": "pillow=枕头，支撑头的软垫",
    "blanket": "blank=白，-et=小，洁白的保暖覆盖物",
    "hat": "hat=帽子，盖在头上的",
    "shirt": "shirt=衬衫，上身穿的短上衣",
    "pant": "pant=下垂裤(古)，s=复数，下垂到腿的裤子",
    "sock": "sock=袜子，s=复数，穿脚上的薄套",
    "jacket": "jack=千斤顶，et=小，短外套",
    "glove": "gl=手，ove=OVE形状，保护手的",
    "scarf": "scar=伤疤，f=形状，像围巾一样围住脖子",
    "umbrella": "umb=阴影，rella=转，遮阳的",
    
    # 食物类
    "apple": "app=应用，le=小，苹果形的小东西",
    "noodles": "noodle=面条，复数形式",
    "tasty": "taste=味道，-y=...的，好味道的",
    "hungry": "hung=hang挂，r=阿姨的谐音，肚子空空的",
    "thirsty": "thirst=渴，-y=...的，口干想喝",
    "spicy": "spice=香料，-y=...的，辣味",
    "yummy": "yum=好吃拟声，-y=...的，真香",
    "meal": "me=我，al=全部，一顿饭",
    "snack": "sn=小，ack=吃，小份食物",
    "drink": "dr=喝，ink=墨水(拟声)，喝的东西",
    "fresh": "fr=fresh新鲜，esh=鱼新鲜，新鲜的",
    "porridge": "por=碗，ridge=脊，粥状食物",
    "cereal": "cer=谷物，eal=吃，谷类早餐",
    "yogurt": "yo=哟，gurt=酸奶油，酸奶",
    "egg": "e=蛋形，gg=两个蛋",
    "rice": "r=米粒，i=一粒，ce=米，发音如米",
    "soup": "so=如此，up=上，热汤",
    "salad": "sal=盐，ad=添加，凉拌菜",
    "chicken": "chick=小鸡，en=的，小鸡肉",
    "beef": "b=牛叫，eef=哞，牛肉",
    "pork": "p=猪叫，ork=哦，猪肉",
    "fish": "fi=fish鱼，sh=鱼游动",
    "vegetable": "veg=蔬菜，etable=可吃的，可吃植物",
    "fruit": "fr=fruit水果，uit=水果成熟",
    "bread": "br=面包烤，ead=面包",
    "cake": "ca=蛋糕，ke=可口，蛋糕",
    "cookie": "co=小，ok=好，ie=好吃，小甜饼",
    "ice cream": "ice=冰，cream=奶油，冰凉甜点",
    "noodle": "no=不，od=饿，le=面，不饿才吃面",
    
    # 日常用品
    "plate": "pla=平，te=托盘，平底盘",
    "bowl": "bo=杯，wl=碗，碗状容器",
    "cup": "cu=杯子，p=杯把，喝水杯",
    "fork": "fo=叉，rk=餐具，叉子",
    "spoon": "sp=勺，oon=长勺，勺子",
    "knife": "kn=切，ife=小刀，切割刀",
    "glass": "gl=玻璃，ass=杯，玻璃杯",
    "napkin": "nap=餐巾，kin=小，擦嘴布",
    "menu": "me=我，nu=看，我看菜谱",
    "bill": "bi=账单，ll=两个零，账单",
    "menu": "men=男人们，u=你，菜单",
    "fridge": "fr=冷，i=冰，dge=储存，冰箱",
    "microwave": "micr=微，o=波，wave=波，微波炉",
    "stove": "st=炉，ove=火，炉子",
    "pan": "pa=平，n=锅，平底锅",
    "pot": "po=锅，t=壶，锅壶",
    
    # 交通类
    "bike": "bi=两，ke=轮，两轮车",
    "traffic": "traff=路，ic=通行，路上的人车",
    "bus": "bu=公共，s=车，公交车",
    "car": "ca=车，r=小，汽车",
    "taxi": "ta=打车，xi=费，打车费",
    "subway": "sub=地下，way=路，地下铁路",
    "train": "tra=运输，in=内部，火车",
    "plane": "pla=平，ne=飞行器，飞机",
    "ship": "shi=船，p=泊，轮船",
    "boat": "bo=船，at=在，船",
    "ticket": "tick=勾，et=小票，票",
    "stop": "st=站，op=停止，站",
    "crowded": "crowd=人群，ed=...的，人多的",
    "far": "fa=远，r=距离，远",
    "near": "ne=近，ar=近的，近",
    "map": "ma=妈，p=地图，地图",
    
    # 地点/人物
    "principal": "prin=首要，cip=领导，al=的，学校领导",
    "teacher": "teach=教，er=人，教书人",
    "student": "stu=学，dent=人，学习者",
    "friend": "fri=friend朋友，end=终，永久的朋友",
    "family": "fa=爸，mi=妈，ly=爱，家人",
    "mom": "mo=妈妈，m=妈，妈妈",
    "dad": "da=爸爸，d=爸，爸爸",
    "grandma": "grand=大，ma=妈，奶奶",
    "grandpa": "grand=大，pa=爷，爷爷",
    "chalk": "cha=粉，lk=块，粉笔",
    "classroom": "class=课，room=房间，教室",
    "library": "lib=书，rary=馆，图书馆",
    "hallway": "hall=大厅，way=路，走廊",
    "ground": "gr=地，ound=地面，地面",
    "hospital": "hospi=客人，tal=地方，医护地",
    
    # 学习类
    "spell": "sp=拼，ell=写字母，拼写",
    "page": "pa=页，ge=页码，页",
    "sentence": "sent=送，ence=状态，完整句子",
    "picture": "pic=画，ture=物品，图画",
    "story": "st=故事，ory=讲，故事书",
    "book": "boo=书，k=知识，书",
    "pencil": "pen=笔，cil=写，画笔",
    "eraser": "e=擦，ras=橡皮，er=器，橡皮",
    "ruler": "ru=尺，ler=测量，尺子",
    "bag": "ba=包，g=袋，书包",
    "homework": "home=家，work=作业，家作业",
    "test": "te=测，st=试，测试",
    "exam": "ex=测试，am=是，考试",
    "lesson": "les=学，son=儿，学习课",
    "class": "cl=课，ass=班级，班课",
    "school": "sch=学，ool=地方，学校",
    "word": "wo=词，rd=读，词汇",
    
    # 动词/动作
    "jump": "ju=跳，mp=跳，跳起",
    "run": "ru=跑，n=跑远，跑步",
    "walk": "wa=走，lk=路，行走",
    "sit": "si=坐，t=椅子，坐",
    "stand": "st=站，and=立，站起",
    "sleep": "sl=睡，eep=休息，睡觉",
    "wake": "wa=醒，ke=起来，醒来",
    "wash": "wa=洗，sh=冲，洗涤",
    "brush": "br=刷，ush=刷子，刷",
    "eat": "ea=吃，t=食物，吃",
    "drink": "dr=喝，ink=喝，喝水",
    "play": "pl=玩，ay=玩要，玩耍",
    "study": "st=学，udy=学习，学习",
    "read": "re=读，ad=看，阅读",
    "write": "wr=写，ite=写字，书写",
    "draw": "dr=画，aw=描，绘画",
    "sing": "si=唱，ng=歌，唱歌",
    "dance": "da=跳，nce=动，跳舞",
    "listen": "lis=听，ten=十，听十次",
    "speak": "sp=说，eak=说话，说话",
    "think": "th=想，ink=思考，思考",
    "look": "lo=看，ok=看好了，看",
    "see": "se=看，e=眼睛，看见",
    "watch": "wa=看，tch=注视，观看",
    "enjoy": "en=使，joy=乐，使享乐",
    "help": "he=帮，lp=助，帮助",
    "cook": "co=厨，ok=做饭，做饭",
    "clean": "cl=清，ean=干净，清洁",
    "open": "op=开，en=门，打开",
    "close": "cl=关，ose=关闭，关闭",
    "start": "st=开，art=开始，开始",
    "stop": "st=停，op=停止，停下",
    "wait": "wa=等，it=它，等待",
    "ask": "as=问，k=问题，询问",
    "answer": "an=答，swer=回答，回答",
    "learn": "le=学，arn=习，学习",
    "teach": "te=教，ach=教给，教书",
    
    # 形容词
    "lazy": "la=懒，zy=自，懒惰的",
    "tired": "ti=累，red=累的精疲力竭",
    "happy": "ha=哈，ppy=开心，哈哈笑",
    "sad": "sa=伤，d=痛，难过的",
    "angry": "an=生气，gry=怒，生气的",
    "scared": "sca=吓，red=怕，害怕的",
    "surprised": "sur=惊，pr=奇，ised=的，惊讶的",
    "beautiful": "beau=美，ti=丽，ful=的，美丽的",
    "ugly": "ug=丑，ly=...的，丑陋的",
    "tall": "ta=高，ll=高个，高",
    "short": "sh=矮，ort=的，矮",
    "big": "bi=大，g=大块，大",
    "small": "sm=小，all=都小，小",
    "long": "lo=长，ng=久，长",
    "new": "ne=新，w=新，新的",
    "old": "ol=老，d=的，老的",
    "good": "goo=好，d=好，好",
    "bad": "ba=坏，d=差，坏",
    "hot": "ho=热，t=烫，热",
    "cold": "co=冷，ld=冷的，冷",
    "warm": "wa=温，rm=暖，温暖",
    "cool": "coo=凉，l=凉，凉快",
    "fast": "fa=快，st=快，迅速",
    "slow": "sl=慢，ow=慢，缓慢",
    "easy": "ea=易，sy=的，容易",
    "difficult": "di=难，ffi=费，cult=苦，难的",
    "right": "ri=对，ght=正确，对的",
    "wrong": "wr=错，ong=误，错误",
    "different": "dif=不同，fer=区别，ent=的，不同",
    "same": "sa=相，me=同，相同",
    "quiet": "qui=静，et=的，安静",
    "noisy": "noi=闹，sy=的，吵闹",
    "clean": "cl=清，ean=干净，清洁",
    "dirty": "di=脏，rty=污的，脏",
    "empty": "em=空，pty=空，满空",
    "full": "fu=满，ll=满，满",
    "safe": "sa=安，fe=全，安全",
    "dangerous": "dan=危，ger=险，ous=的，危险",
    
    # 名词
    "time": "ti=时，me=刻，时间",
    "day": "da=日，y=日，日",
    "night": "ni=夜，ght=黑，夜晚",
    "morning": "mo=早，rning=晨，清晨",
    "afternoon": "af=午，ternoon=下午，下午",
    "evening": "ev=晚，ening=间，傍晚",
    "today": "to=今，day=日，今天",
    "tomorrow": "to=明，morrow=天，明天",
    "yesterday": "yes=昨，ter=天，day=日，昨天",
    "week": "we=周，ek=期，周",
    "month": "mo=月，nth=月份，月",
    "year": "ye=年，ar=年，年",
    "hour": "ho=时，ur=时间，时",
    "minute": "mi=分，nute=分钟，分",
    "second": "se=秒，cond=秒，秒",
    "weather": "we=天气，ather=气候，天气",
    "color": "co=颜，lor=色，颜色",
    "number": "nu=数，mber=字，数字",
    "friend": "fri=朋，end=友，朋友",
    "name": "na=名，me=字，名字",
    "age": "ag=年，e=龄，年龄",
    "birthday": "birth=出生，day=日，生日",
    "party": "pa=派，rty=聚会，聚会",
    "game": "ga=游，me=戏，游戏",
    "song": "so=歌，ng=曲，歌曲",
    "music": "mu=音，sic=乐，音乐",
    "movie": "mo=电，vie=影，电影",
    "photo": "ph=照，oto=片，照片",
    "toy": "to=玩，y=物，玩具",
    "gift": "gi=礼，ft=物，礼物",
    "money": "mo=钱，ney=币，金钱",
    "price": "pr=价，ice=价，价格",
    "store": "st=商，ore=店，商店",
    "market": "ma=市，rket=场，市场",
    "restaurant": "rest=休息，au=吃，rant=地方，餐馆",
    "hospital": "hospi=护理，tal=地方，医院",
    "park": "pa=公，rk=园，公园",
    "zoo": "zo=动，o=园，动物园",
    "beach": "bea=海，ch=滩，海滩",
    "mountain": "moun=山，tain=峰，山",
    "river": "ri=河，ver=流，河流",
    "lake": "la=湖，ke=泊，湖泊",
    "tree": "tr=树，ee=绿，树",
    "flower": "flo=花，wer=朵，花",
    "grass": "gr=草，ass=草场，草",
    "animal": "an=动，imal=物，动物",
    "bird": "bi=鸟，rd=鸟，鸟",
    "cat": "ca=猫，t=猫叫，猫",
    "dog": "do=狗，g=狗叫，狗",
    "fish": "fi=鱼，sh=鱼游，鱼",
    
    # 时间/日期
    "Monday": "Mon=周一，day=天，周一",
    "Tuesday": "Tues=周二，day=天，周二",
    "Wednesday": "Weds=周三，day=天，周三",
    "Thursday": "Thurs=周四，day=天，周四",
    "Friday": "Fri=周五，day=天，周五",
    "Saturday": "Sat=周六，urday=天，周六",
    "Sunday": "Sun=周日，day=天，周日",
    "January": "Jan=一月，uary=月，一月",
    "February": "Feb=二月，ruary=月，二月",
    "March": "Mar=三月，ch=月，三月",
    "April": "Apr=四月，il=月，四月",
    "May": "Ma=五月，y=月，五月",
    "June": "Ju=六月，ne=月，六月",
    "July": "Jul=七月，y=月，七月",
    "August": "Au=八月，gust=热月，八月",
    "September": "Sep=九月，tember=月，九月",
    "October": "Oct=十月，ober=月，十月",
    "November": "Nov=十一月，ember=月，十一月",
    "December": "Dec=十二月，ember=月，十二月",
    
    # 其他常用词
    "please": "pl=请，ease=容易，请便",
    "thanks": "th=谢，anks=谢，感谢",
    "sorry": "so=对，rry=不起，对不起",
    "hello": "he=你，llo=好，你好",
    "goodbye": "good=好，bye=再见，再见",
    "welcome": "wel=好，come=来，欢迎",
    "again": "ag=再，ain=一次，再一次",
    "always": "al=总，ways=方式，总是",
    "never": "ne=从，ver=未，从不",
    "sometimes": "som=有时，etimes=次，有时",
    "often": "of=常，ten=常，经常",
    "still": "st=仍，ill=还，仍然",
    "already": "al=已，ready=准备好，已完成",
    "enough": "en=足，ough=够，足够",
    "more": "mo=更，re=多，更多",
    "less": "le=少，ss=少，更少",
    "most": "mo=最，st=多，最多",
    "all": "al=全，l=都，全部",
    "each": "ea=每，ch=个，每个",
    "every": "ev=每，ery=都，每个",
    "both": "bo=两，th=者，两者",
    "either": "ei=任，ther=一，任一",
    "neither": "ne=否，i=任，ther=一，两者都不",
    "other": "ot=其，her=他，其他的",
    "another": "an=再，other=一个，再一个",
    "something": "some=某，thing=物，某物",
    "anything": "any=任，thing=物，任何物",
    "nothing": "no=无，thing=物，无物",
    "everything": "every=每，thing=物，一切",
    "someone": "some=某，one=人，某人",
    "anyone": "any=任，one=人，任何人",
    "everyone": "every=每，one=人，每人",
    "myself": "my=我，self=自己，我自己",
    "yourself": "your=你，self=自己，你自己",
    "himself": "him=他，self=自己，他自己",
    "herself": "her=她，self=自己，她自己",
    
    # 学校相关
    "study": "stu=学，dy=习，学习",
    "learn": "lea=学，rn=习，学会",
    "practice": "prac=练习，tice=做，练习",
    "homework": "home=家，work=作业，家庭作业",
    "test": "tes=测，t=试，测试",
    "quiz": "qu=问，iz=测，小测验",
    "homework": "home=家，work=工作，家作业",
    "problem": "pro=问题，blem=困难，问题",
    "question": "quest=问，ion=问题，提问",
    "answer": "ans=答，wer=答，回答",
    "example": "exa=例子，mple=示范，例子",
    "lesson": "les=学，son=习，课",
    "class": "cla=课，ss=班级，班",
    "grade": "gr=年，ade=级，年级",
    "subject": "sub=科目，ject=主题，科目",
    "science": "sci=科，ence=学问，科学",
    "math": "ma=数，th=学，数学",
    "history": "his=历，tory=故事，历史",
    "geography": "geo=地，graphy=记录，地理",
    "art": "ar=艺，t=术，艺术",
    "music": "mu=音，sic=乐，音乐",
    "PE": "PE=体育，physical=身体，education=教育",
    "subject": "sub=主题，ject=投射，学科",
    "homework": "home=家，work=事，家庭作业",
    "project": "pro=项目，ject=投，项目",
    "team": "te=团，am=队，团队",
    "partner": "part=部分，ner=人，搭档",
    
    # 职业/身份
    "doctor": "do=做，ctor=者，医生",
    "nurse": "nu=护，rse=士，护士",
    "teacher": "teach=教，er=人，教师",
    "student": "stu=学，dent=人，学生",
    "driver": "dri=驾，ver=者，司机",
    "cook": "coo=厨，k=师，厨师",
    "farmer": "farm=农，er=人，农民",
    "worker": "work=工，er=人，工人",
    "businessman": "business=商业，man=人，商人",
    "policeman": "police=警察，man=人，警察",
    "fireman": "fire=火，man=人，消防员",
    "postman": "post=邮，man=人，邮递员",
    "waiter": "wait=等，er=人，服务员",
    "secretary": "secre=秘，tary=员，秘书",
    "manager": "man=管，ager=理人，经理",
    "salesman": "sale=卖，sman=人，售货员",
    "engineer": "en=工程，gine=机，er=人，工程师",
    "artist": "art=艺，ist=家，艺术家",
    "scientist": "sci=科，entist=家，科学家",
    "writer": "wri=写，ter=人，作家",
    "singer": "sin=唱，ger=人，歌手",
    "actor": "act=演，or=者，演员",
    "actress": "act=演，ress=女，女演员",
    
    # 身体部位
    "head": "he=头，ad=头部，头",
    "face": "fa=面，ce=脸，脸",
    "eye": "ey=眼，e=眼睛，眼",
    "ear": "ea=耳，r=耳，耳",
    "nose": "no=鼻，se=鼻，鼻",
    "mouth": "mo=嘴，uth=口，嘴",
    "tooth": "to=牙，oth=齿，牙",
    "teeth": "tee=牙，th=复数，teeth牙齿",
    "hand": "ha=手，nd=手部，手",
    "foot": "fo=脚，ot=足，脚",
    "feet": "fe=脚，et=复数，脚",
    "finger": "fin=指，ger=手指，手指",
    "hair": "ha=发，ir=发，发",
    "neck": "ne=颈，ck=脖子，颈",
    "stomach": "stom=胃，ach=痛，胃",
    
    # 天气/自然
    "sunny": "sun=太阳，ny=...的，晴朗",
    "cloudy": "cloud=云，y=...的，多云",
    "rainy": "rain=雨，y=...的，下雨",
    "snowy": "snow=雪，y=...的，下雪",
    "windy": "wind=风，y=...的，有风",
    "hot": "ho=热，t=温度高，热",
    "cold": "co=冷，ld=温度低，冷",
    "warm": "wa=温，rm=暖，温暖",
    "cool": "coo=凉，l=凉爽，凉",
    "spring": "sp=春，ring=季，春天",
    "summer": "su=夏，mmer=季，夏天",
    "autumn": "au=秋，tumn=季，秋天",
    "winter": "wi=冬，nter=季，冬天",
    "rain": "ra=雨，in=下，下雨",
    "snow": "sn=雪，ow=下，下雪",
    "wind": "wi=风，nd=吹，风",
    "cloud": "clo=云，ud=云，云",
    
    # 家庭/房间
    "house": "ho=房，use=屋，房子",
    "home": "ho=家，me=我，我家",
    "room": "ro=房，om=间，房间",
    "kitchen": "kit=厨，chen=间，厨房",
    "bathroom": "bath=浴，room=室，浴室",
    "bedroom": "bed=床，room=室，卧室",
    "living room": "liv=客，ing=厅，客厅",
    "garden": "gar=花，den=园，花园",
    "door": "do=门，or=口，门",
    "window": "win=窗，dow=口，窗",
    "floor": "flo=地，or=板，地板",
    "wall": "wa=墙，ll=壁，墙",
    "table": "ta=桌，ble=台，桌子",
    "chair": "ch=椅，air=座，椅子",
    "desk": "de=书，sk=桌，书桌",
    "bed": "be=床，d=铺，床",
    "sofa": "so=沙，fa=发，沙发",
    "TV": "T=电，V=视，电视",
    "computer": "com=电脑，put=计算，er=器，电脑",
    "phone": "ph=电，one=话，电话",
    "clock": "clo=钟，ck=时间，钟",
    "photo": "ph=照，oto=片，照片",
    
    # 健康/感觉
    "headache": "head=头，ache=痛，头痛",
    "stomachache": "stom=胃，ach=痛，胃痛",
    "toothache": "tooth=牙，ache=痛，牙痛",
    "fever": "fe=发，ver=热，发烧",
    "cough": "co=咳，ugh=嗽，咳嗽",
    "cold": "co=冷，ld=病，感冒",
    "hospital": "hospi=护理，tal=地方，医院",
    "medicine": "med=药，icine=学，药",
    "doctor": "do=医，ctor=生，医生",
    "pain": "pa=痛，in=疼，疼",
    "hurt": "hu=伤，rt=痛，受伤",
    "tired": "ti=累，red=疲，累",
    "ill": "i=病，ll=病，生病",
    "well": "we=好，ll=健康，健康",
    "sick": "si=病，ck=的，生病",
    "fine": "fi=好，ne=的，好",
    
    # 活动/爱好
    "swim": "sw=游，im=泳，游泳",
    "play": "pl=玩，ay=戏，玩耍",
    "game": "ga=游，me=戏，游戏",
    "sport": "sp=体，ort=动，体育",
    "hobby": "ho=业，bby=爱好，爱好",
    "collect": "col=收，lect=集，收集",
    "paint": "pa=画，int=涂，画画",
    "read": "re=读，ad=看，阅读",
    "write": "wr=写，ite=写，写作",
    "draw": "dr=画，aw=绘，画",
    "sing": "si=唱，ng=歌，唱",
    "dance": "da=跳，nce=舞，跳",
    "ride": "ri=骑，de=车，骑",
    "climb": "cl=爬，imb=山，爬",
    "fly": "fl=飞，y=飞，飞",
    "skate": "sk=滑，ate=滑，滑冰",
    "ski": "sk=滑，i=雪，滑雪",
    "surf": "su=冲，rf=浪，冲浪",
    
    # 学校物品
    "pencil": "pen=笔，cil=尖，铅笔",
    "pen": "pe=笔，n=尖，笔",
    "eraser": "e=擦，ras=橡，er=器，橡皮",
    "ruler": "ru=尺，ler=量，直尺",
    "bag": "ba=包，g=袋，包",
    "book": "boo=书，k=本，书",
    "notebook": "note=笔记，book=本，笔记本",
    "dictionary": "dic=词，tionary=典，词典",
    "map": "ma=图，p=地图",
    "chalk": "cha=粉，lk=笔，粉笔",
    "blackboard": "black=黑，board=板，黑板",
    "desk": "de=书，sk=桌，书桌",
    "chair": "ch=椅，air=座，椅子",
    "classroom": "class=课，room=室，教室",
    "library": "lib=书，rary=馆，图书馆",
    "playground": "play=玩，ground=地，操场",
    
    # 社交/情感
    "love": "lo=爱，ve=爱，爱",
    "like": "li=喜，ke=欢，喜欢",
    "hate": "ha=恨，te=讨厌，恨",
    "happy": "ha=开，ppy=心，开心",
    "sad": "sa=伤，d=痛，难过",
    "angry": "an=生，gry=气，生气",
    "excited": "ex=兴，cit=奋，ed=的，兴奋",
    "worried": "wo=担，rr=忧，ied=的，担心",
    "surprised": "sur=惊，pr=讶，ised=的，惊讶",
    "proud": "pr=骄，oud=傲，骄傲",
    "shy": "sh=羞，y=的，害羞",
    "friendly": "friend=朋友，ly=...的，友好",
    "funny": "fun=有趣，ny=的，有趣",
    "crazy": "cr=疯，azy=狂，疯狂",
    "polite": "po=礼，lite=貌，有礼貌",
    "rude": "ru=粗，de=鲁，粗鲁",
    "honest": "ho=诚，nest=实，诚实",
    "brave": "br=勇，ave=敢，勇敢",
    "clever": "cl=聪，ever=明，聪明",
    "stupid": "st=笨，upid=愚，笨",
    
    # 方向/位置
    "left": "le=左，ft=边，左",
    "right": "ri=右，ght=边，右",
    "up": "u=上，p=上，向上",
    "down": "do=下，wn=下，向下",
    "front": "fr=前，ont=面，前面",
    "back": "ba=后，ck=面，后面",
    "top": "to=上，p=顶，顶",
    "bottom": "bo=底，ttom=部，底部",
    "side": "si=旁，de=边，边",
    "middle": "mi=中，ddle=间，中间",
    "center": "cen=中，ter=心，中心",
    "outside": "out=外，side=侧，外面",
    "inside": "in=内，side=侧，里面",
    "here": "he=这，re=里，这里",
    "there": "th=那，ere=里，那里",
    "where": "wh=哪，ere=里，哪里",
    
    # 颜色
    "red": "r=红，ed=色，红色",
    "blue": "bl=蓝，ue=色，蓝色",
    "green": "gr=绿，een=色，绿色",
    "yellow": "ye=黄，llow=色，黄色",
    "orange": "or=橙，ange=色，橙色",
    "purple": "pu=紫，rple=色，紫色",
    "pink": "pi=粉，nk=色，粉色",
    "brown": "br=棕，own=色，棕色",
    "black": "bl=黑，ack=色，黑色",
    "white": "wh=白，ite=色，白色",
    "gray": "gr=灰，ay=色，灰色",
    "color": "co=颜，lor=色，颜色",
    
    # 数字
    "one": "o=1，ne=一，一",
    "two": "tw=2，o=二，二",
    "three": "thr=3，ee=三，三",
    "four": "fo=4，ur=四，四",
    "five": "fi=5，ve=五，五",
    "six": "si=6，x=六，六",
    "seven": "se=7，ven=七，七",
    "eight": "ei=8，ght=八，八",
    "nine": "ni=9，ne=九，九",
    "ten": "te=10，n=十，十",
    "eleven": "el=11，even=偶，十一点",
    "twelve": "tw=12，elve=十，二十",
    "twenty": "twent=二十，y=十，二十",
    "hundred": "hun=百，dred=百，百",
    "thousand": "thou=千，sand=千，千",
    "million": "mil=百，lion=万，百万",
    
    # 日常对话
    "please": "pl=请，ease=容易，请",
    "thanks": "th=谢，anks=谢，谢谢",
    "sorry": "so=对，rry=不起，对不起",
    "excuse": "ex=借，cuse=口，借过",
    "help": "he=帮，lp=助，帮助",
    "wait": "wa=等，it=它，等",
    "stop": "st=停，op=止，停止",
    "start": "st=开，art=始，开始",
    "try": "tr=试，y=一下，尝试",
    "finish": "fi=完，nish=结束，完成",
    "continue": "con=继，tinue=续，继续",
    "remember": "re=再，member=成员，想起",
    "forget": "for=忘，get=得到，忘记",
    "know": "kn=知，ow=道，知道",
    "think": "th=想，ink=思考，想",
    "believe": "be=相，lieve=信，相信",
    "understand": "un=明，der=理，stand=理解，领会",
    "mean": "me=意，an=思，意思是",
    "want": "wa=想，nt=要，想要",
    "need": "ne=需，ed=要，需要",
    "like": "li=喜，ke=欢，喜欢",
    "love": "lo=爱，ve=爱，爱",
    "hate": "ha=恨，te=讨厌，恨",
    "hope": "ho=希，pe=望，希望",
    "wish": "wi=祝，sh=福，祝愿",
    "decide": "de=决，cide=定，决定",
    "plan": "pl=计，an=划，计划",
    "agree": "ag=同，ree=意，同意",
    "disagree": "dis=不，agree=同意，不同意",
    
    # 其他常见词
    "because": "be=因，cause=为，因为",
    "although": "al=虽，though=然，虽然",
    "however": "how=如，ever=何，然而",
    "therefore": "the=因，re=此，fore=故，因此",
    "perhaps": "per=可，haps=能，也许",
    "maybe": "ma=可，ybe=许，也许",
    "probably": "pro=可，bably=能，大概",
    "certainly": "cer=肯，tain=定，ly=地，当然",
    "exactly": "ex=正，actly=确，正好",
    "really": "re=真，ally=实，真的",
    "very": "ve=很，ry=的，非常",
    "quite": "qu=相，i=当，te=的，相当",
    "rather": "rat=相，her=当，相当",
    "almost": "al=几，most=乎，几乎",
    "nearly": "ne=近，arly=乎，将近",
    "only": "on=仅，ly=地，只有",
    "just": "ju=刚，st=好，正好",
    "still": "st=仍，ill=然，仍然",
    "already": "al=已，ready=好，已经",
    "yet": "ye=还，t=未，还未",
    "soon": "so=马，on=上，马上",
    "later": "la=稍，ter=后，稍后",
    "early": "ea=早，rly=地，早",
    "late": "la=晚，te=迟，迟",
    "quick": "qu=快，ick=速，快",
    "slow": "sl=慢，ow=慢，慢",
    "together": "to=到，gether=一起，一起",
    "alone": "al=单，one=人，独自",
    "outside": "out=外，side=面，外面",
    "inside": "in=内，side=面，里面",
    "around": "a=四，round=围，四周",
    "between": "be=在，tween=两者间，两者之间",
    "among": "am=在，ong=多...中，在...中",
    
    # 常用动词短语
    "get up": "get=起来，up=上，起床",
    "wake up": "wake=醒，up=来，醒来",
    "put on": "put=穿，on=上，穿上",
    "take off": "take=脱，off=掉，脱下",
    "go to bed": "go=去，bed=床，睡觉",
    "fall asleep": "fall=倒，asleep=睡，睡着",
    "brush teeth": "brush=刷，teeth=牙，刷牙",
    "wash face": "wash=洗，face=脸，洗脸",
    "comb hair": "comb=梳，hair=发，梳头",
    "get dressed": "get=穿好，dressed=衣服，穿好衣服",
    "have breakfast": "have=吃，breakfast=早餐，吃早饭",
    "have lunch": "have=吃，lunch=午餐，吃午饭",
    "have dinner": "have=吃，dinner=晚餐，吃晚饭",
    "go to school": "go=去，school=学校，上学",
    "go home": "go=回，home=家，回家",
    "come back": "come=来，back=回，回来",
    "look at": "look=看，at=向，看",
    "listen to": "listen=听，to=着，听",
    "talk to": "talk=谈，to=与，谈",
    "wait for": "wait=等，for=着，等候",
    "look for": "look=找，for=着，寻找",
    "find out": "find=找，out=出，发现",
    "put away": "put=放，away=走，放好",
    "pick up": "pick=捡，up=起，拾起",
    "give up": "give=放，up=弃，放弃",
    "turn on": "turn=开，on=启，打开",
    "turn off": "turn=关，off=闭，关掉",
    "show up": "show=显，up=现，出现",
    "grow up": "grow=长，up=大，长大",
    "cheer up": "cheer=振，up=起，振作",
    "clean up": "clean=清，up=洁，收拾干净",
    "set up": "set=设，up=立，建立",
    "make up": "make=做，up=成，组成",
    "come up with": "come=想，up=出，with=到，想出",
    "get along with": "get=相，along=处，with=与，相处",
    "look forward to": "look=期，forward=望，to=着，期待",
    "take care of": "take=照，care=顾，of=料，照料",
    "pay attention to": "pay=注，attention=意，to=意，注意",
    "take part in": "take=参，part=加，in=与，参加",
    "catch up with": "catch=追，up=上，with=上，赶超",
    "keep in touch with": "keep=保，in=联，touch=系，with=与，保持联系",
}

def fix_memory_tip(content, word, zh_meaning):
    """为给定词生成更好的记忆提示"""
    word_lower = word.lower()
    
    # 如果在字典中找到，直接返回
    if word_lower in MEMORY_TIPS:
        return MEMORY_TIPS[word_lower]
    
    # 否则根据规则生成
    # 常见后缀
    suffixes = {
        's': '', 'es': '', 'ed': '', 'ing': '', 'ly': '', 
        'tion': '', 'sion': '', 'ness': '', 'ment': '',
        'able': '', 'ible': '', 'ful': '', 'less': '',
        'ous': '', 'ive': '', 'al': '', 'ial': '',
        'er': '', 'est': '', 'ist': '', 'ian': '',
        'age': '', 'ure': '', 'ure': '',
    }
    
    # 常见前缀
    prefixes = {
        'un': '', 're': '', 'dis': '', 'mis': '',
        'over': '', 'under': '', 'out': '', 'im': '',
        'in': '', 'il': '', 'ir': '', 'pre': '',
        'post': '', 'ex': '', 'anti': '', 'auto': '',
    }
    
    # 生成基于构词法的提示
    for pre, pre_meaning in prefixes.items():
        if word_lower.startswith(pre):
            rest = word_lower[len(pre):]
            return f"{pre}({pre_meaning}) + {rest} = {zh_meaning}"
    
    for suff, suff_meaning in suffixes.items():
        if word_lower.endswith(suff):
            base = word_lower[:-len(suff)] if len(suff) > 1 else word_lower[:-1]
            return f"{base} + {suff}({suff_meaning}) = {zh_meaning}"
    
    # 默认：基于发音或简单拆解
    if len(word_lower) <= 4:
        return f"{word_lower}：多读几遍，体会发音"
    else:
        mid = len(word_lower) // 2
        part1, part2 = word_lower[:mid], word_lower[mid:]
        return f"拆开记：{part1} + {part2}"


def fix_html_file(filepath):
    """修复单个HTML文件的记忆提示"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # 1. 修复"记住xxx的英文表达"格式
    pattern1 = r'记住''(.*?)''的英文表达'
    matches = re.findall(pattern1, content)
    for word in matches:
        old_pattern = f"记住'{word}'的英文表达"
        # 尝试从HTML中找到对应的中文意思
        zh_pattern = rf'class="word-title">({re.escape(word)})</span>.*?class="chinese-meaning">([^<]+)</span>'
        zh_match = re.search(zh_pattern, content)
        if zh_match:
            zh = zh_match.group(2)
        else:
            zh = word
        new_tip = fix_memory_tip(content, word, zh)
        new_tip = f"{word}：{new_tip}"
        if old_pattern in content:
            content = content.replace(old_pattern, new_tip)
            modified = True
    
    # 2. 修复简单的"xxx=yyy"格式记忆提示
    pattern2 = r'([^：]+)=([^，,]+)[，,]?([^<]*?)</div>'
    
    def replace_simple_tip(match):
        word_part = match.group(1)
        zh_part = match.group(2)
        extra = match.group(3)
        
        # 如果记忆提示只有"xxx=yyy"或类似格式，则改进它
        if len(extra.strip()) <= 2 or extra.strip() in ['。', '']:
            word = word_part.strip()
            new_tip = fix_memory_tip(content, word, zh_part)
            return f"{word}：{new_tip}</div>"
        return match.group(0)
    
    new_content = re.sub(pattern2, replace_simple_tip, content)
    if new_content != content:
        content = new_content
        modified = True
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return modified


def main():
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    # 获取所有HTML文件
    html_files = glob.glob('2026-*.html') + glob.glob('2027-*.html')
    html_files.sort()
    
    fixed_count = 0
    for filepath in html_files:
        if fix_html_file(filepath):
            fixed_count += 1
            print(f"[OK] {filepath}")
        else:
            print(f"[--] {filepath}")
    
    print(f"\nTotal: Fixed {fixed_count} files")


if __name__ == '__main__':
    main()
