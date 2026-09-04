# -*- coding: utf-8 -*-
"""seed_products

内存商品库的种子数据：10 个跨境 SPU，覆盖旅行装备、数码配件、家居等品类，
中文标题 + 关键词化描述，便于关键词召回命中"抗造 / 轻便 / 不要塑料"这类口语属性词。
"""
from __future__ import annotations

from app.domain.catalog.money import Money
from app.domain.catalog.product import Product, ProductHighlight
from app.domain.catalog.sku import Sku


def _sku(sku_id: str, spec: str, major: float, currency: str, stock: int) -> Sku:
    return Sku(sku_id=sku_id, spec=spec, price=Money.from_major_units(major, currency), stock=stock)


def build_seed_products() -> list[Product]:
    return [
        Product(
            product_id="P1001",
            title="Nomadica 旅行三件套（收纳袋+颈枕+眼罩）",
            brand="Nomadica",
            category="旅行装备",
            origin_country="VN",
            description="帆布加尼龙材质 结实耐磨 抗造 轻便 无塑料感 小众设计师品牌 适合长途飞行 旅行收纳",
            highlights=[
                ProductHighlight("材质", "帆布+再生尼龙，非塑料"),
                ProductHighlight("重量", "全套 420g 轻便"),
                ProductHighlight("风格", "小众设计师联名款"),
            ],
            ships_to=["CN", "US", "SG"],
            skus=[
                _sku("P1001-S1", "军绿色", 189.0, "CNY", 50),
                _sku("P1001-S2", "沙漠黄", 199.0, "CNY", 30),
            ],
        ),
        Product(
            product_id="P1002",
            title="TrailOx 20寸登机行李箱 铝框款",
            brand="TrailOx",
            category="旅行装备",
            origin_country="DE",
            description="铝镁合金框架 PC箱体 结实抗摔 抗造 万向静音轮 TSA海关锁 登机尺寸 商务旅行",
            highlights=[
                ProductHighlight("箱体", "德国工艺铝框，抗摔"),
                ProductHighlight("轮组", "日本静音万向轮"),
            ],
            ships_to=["CN", "US", "EU"],
            skus=[
                _sku("P1002-S1", "银色 / 20寸", 899.0, "CNY", 20),
                _sku("P1002-S2", "黑色 / 20寸", 899.0, "CNY", 15),
            ],
        ),
        Product(
            product_id="P1003",
            title="Wanderlite 折叠旅行双肩包 35L",
            brand="Wanderlite",
            category="旅行装备",
            origin_country="KR",
            description="防泼水尼龙 超轻 可折叠收纳 大容量 35升 徒步 城市通勤 便宜实惠 高性价比",
            highlights=[
                ProductHighlight("重量", "仅 380g 超轻"),
                ProductHighlight("收纳", "可折叠成手掌大小"),
            ],
            ships_to=["CN", "JP", "SG"],
            skus=[
                _sku("P1003-S1", "石墨黑", 129.0, "CNY", 80),
                _sku("P1003-S2", "雾霾蓝", 129.0, "CNY", 60),
            ],
        ),
        Product(
            product_id="P1004",
            title="AeroHush 主动降噪蓝牙耳机 Pro",
            brand="AeroHush",
            category="数码配件",
            origin_country="US",
            description="主动降噪 蓝牙5.4 40小时续航 通话降噪 飞行旅行伴侣 头戴式 折叠便携",
            highlights=[
                ProductHighlight("降噪", "-45dB 深度主动降噪"),
                ProductHighlight("续航", "40 小时长续航"),
            ],
            ships_to=["CN", "US", "EU"],
            skus=[
                _sku("P1004-S1", "曜石黑", 219.0, "USD", 40),
                _sku("P1004-S2", "月光白", 229.0, "USD", 25),
            ],
        ),
        Product(
            product_id="P1005",
            title="VoltTrek 65W 氮化镓旅行充电器（全球插脚）",
            brand="VoltTrek",
            category="数码配件",
            origin_country="CN",
            description="氮化镓 GaN 65W 快充 全球通用插脚 英标欧标美标 出国旅行 多口 Type-C 轻巧",
            highlights=[
                ProductHighlight("插脚", "全球 150+ 国家通用"),
                ProductHighlight("功率", "65W 双口快充"),
            ],
            ships_to=["CN", "US", "EU", "JP"],
            skus=[
                _sku("P1005-S1", "标准版", 159.0, "CNY", 100),
            ],
        ),
        Product(
            product_id="P1006",
            title="TerraCotta 手工粗陶旅行茶具套装",
            brand="TerraCotta",
            category="家居生活",
            origin_country="JP",
            description="手工粗陶 一壶两杯 便携旅行装 无塑料 天然材质 小众手作 茶道 送礼",
            highlights=[
                ProductHighlight("材质", "天然粗陶，无塑料"),
                ProductHighlight("工艺", "日本手作窑烧"),
            ],
            ships_to=["CN", "JP"],
            skus=[
                _sku("P1006-S1", "原色", 268.0, "CNY", 18),
            ],
        ),
        Product(
            product_id="P1007",
            title="PeakDry 速干旅行毛巾三件装",
            brand="PeakDry",
            category="旅行装备",
            origin_country="TW",
            description="超细纤维 速干 轻薄 抗菌 三条装 大中小 游泳 健身 户外 便宜 高性价比",
            highlights=[
                ProductHighlight("速干", "3 分钟拧干即用"),
                ProductHighlight("装量", "大中小三条装"),
            ],
            ships_to=["CN", "US", "SG"],
            skus=[
                _sku("P1007-S1", "灰蓝绿三色", 79.0, "CNY", 200),
            ],
        ),
        Product(
            product_id="P1008",
            title="LumenGo 便携露营灯 可充电",
            brand="LumenGo",
            category="户外运动",
            origin_country="CN",
            description="露营灯 三档调光 Type-C充电 磁吸挂钩 防水 IPX5 户外 应急 停电 抗造耐摔",
            highlights=[
                ProductHighlight("防护", "IPX5 防水，抗摔"),
                ProductHighlight("续航", "最长 72 小时"),
            ],
            ships_to=["CN", "US", "EU"],
            skus=[
                _sku("P1008-S1", "军绿", 89.0, "CNY", 150),
                _sku("P1008-S2", "橙色", 89.0, "CNY", 90),
            ],
        ),
        Product(
            product_id="P1009",
            title="SilkRoute 桑蚕丝旅行睡袋内胆",
            brand="SilkRoute",
            category="旅行装备",
            origin_country="CN",
            description="100%桑蚕丝 亲肤 隔脏 超轻 200g 卷收便携 酒店青旅 露营 天然材质 无塑料",
            highlights=[
                ProductHighlight("材质", "100% 桑蚕丝，天然无塑料"),
                ProductHighlight("重量", "仅 200g"),
            ],
            ships_to=["CN", "US", "EU", "JP"],
            skus=[
                _sku("P1009-S1", "本白", 329.0, "CNY", 35),
            ],
        ),
        Product(
            product_id="P1010",
            title="CascadePro 钛合金折叠登山杖一对",
            brand="CascadePro",
            category="户外运动",
            origin_country="US",
            description="钛合金 折叠五节 快锁 减震 徒步 登山 结实抗造 轻量 260g单支 专业户外",
            highlights=[
                ProductHighlight("材质", "航空钛合金，结实抗造"),
                ProductHighlight("折叠", "五节折叠仅 36cm"),
            ],
            ships_to=["US", "CN", "EU"],
            skus=[
                _sku("P1010-S1", "钛原色一对", 149.0, "USD", 22),
            ],
        ),
    ]
