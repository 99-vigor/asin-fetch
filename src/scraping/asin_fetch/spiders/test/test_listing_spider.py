from ..listing_spider import ListingSpider
from scrapy.http import HtmlResponse, Request
import os
import sys

def test_extract_asin():
    spider = ListingSpider(asin="B002QYW8LW")
    result = spider.extract_asin("https://www.amazon.com/dp/B002QYW8LW")
    assert result == "B002QYW8LW"

def test_extract_asin_too_short():
    spider = ListingSpider(asin="B002QYW8L")
    result = spider.extract_asin("https://www.amazon.com/dp/B002QYW8L")
    assert result == None

def test_extract_categories():
    spider = ListingSpider(asin="")
    mock_response = HtmlResponse(url='', body="""
        <div id="wayfinding-breadcrumbs_container">
            <div id="wayfinding-breadcrumbs_feature_div">
                <ul class="a-unordered-list a-horizontal a-size-small">
                    <li><span class="a-list-item"><a href="">Baby Products</a></span></li>
                    <li class="a-breadcrumb-divider"><span>›</span></li>
                    <li><span class="a-list-item"><a href="">Baby Care</a></span></li>
                    <li class="a-breadcrumb-divider"><span>›</span></li>
                    <li><span class="a-list-item"><a href="">Pacifiers, Teethers &amp; Teething Relief</a></span></li>
                    <li class="a-breadcrumb-divider"><span>›</span></li>
                    <li><span class="a-list-item"><a href="">Teethers</a></span></li>
                </ul>
            </div>
        </div>
    """, encoding='utf-8')
    result = spider.extract_categories(mock_response.selector)
    assert result == ['Baby Products', 'Baby Care', 'Pacifiers, Teethers & Teething Relief', 'Teethers']

def test_extract_dimensions_tableform():
    spider = ListingSpider(asin="")
    mock_response = HtmlResponse(url='', body="""
        <div id="prodDetails">
            <a id="productDetails" name="productDetails" aria-hidden="true"></a>
            <h2>Product information</h2>
            <div class="disclaim">Color: <strong>Yellow</strong></div>
            <div class="wrapper USlocale">
                <div class="column col1 ">
                    <div class="section techD">
                        <div class="secHeader">
                            <span>Technical Details</span>
                        </div>
                        <div class="content pdClearfix">
                            <div class="attrG" style="border:none">
                                <div class="pdTab" style="display:block;">
                                    <table cellspacing="0" cellpadding="0" border="0">
                                        <tbody>
                                            <tr class="size-weight"><td class="label">Item Weight</td><td class="value">1.44 ounces</td></tr>
                                            <tr class="size-weight"><td class="label">Product Dimensions</td><td class="value">4.3 x 0.4 x 7.9 inches</td></tr>
                                            <tr class="item-model-number"><td class="label">Item model number</td><td class="value">BR003</td></tr>
                                            <tr><td class="label">Target gender</td><td class="value">Unisex</td></tr>
                                            <tr><td class="label">Material Type</td><td class="value">Silicone</td></tr>
                                            <tr><td class="label">Number of items</td><td class="value">1</td></tr>
                                            <tr><td class="label">Batteries required</td><td class="value">No</td></tr>
                                            <tr><td class="label">Dishwasher safe</td><td class="value">No</td></tr>
                                            <tr><td class="label">Is portable</td><td class="value">No</td></tr>
                                            <tr><td class="lAttr">&nbsp;</td><td class="lAttr">&nbsp;</td></tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    """, encoding='utf-8')
    result = spider.extract_dimensions_tableform(mock_response.selector)
    assert result == "4.3 x 0.4 x 7.9 inches"

def test_extract_rank_tableform():
    spider = ListingSpider(asin="")
    mock_response = HtmlResponse(url='', body="""
        <tbody>
            <tr><td class="label">ASIN</td><td class="value">B002QYW8LW</td></tr>
            <tr id="SalesRank">
                <td class="label">Amazon Best Sellers Rank</td>
                <td class="value">
                    #33 in Baby (<a href="">See Top 100 in Baby</a>)
                    <ul class="zg_hrsr">
                        <li class="zg_hrsr_item">
                            <span class="zg_hrsr_rank">#2</span>
                            <span class="zg_hrsr_ladder">in <a href="">Baby Health Care Products</a></span>
                        </li>
                        <li class="zg_hrsr_item">
                            <span class="zg_hrsr_rank">#2</span>
                            <span class="zg_hrsr_ladder">in <a href="">Baby Teether Toys</a></span>
                        </li>
                    </ul>
                </td>
            </tr>
            <tr class="shipping-weight">
                <td class="label">Shipping Weight</td>
                <td class="value">1.4 ounces (<a href="">View shipping rates and policies</a>)</td>
            </tr>
        </tbody>
    """, encoding='utf-8')
    result = spider.extract_rank_tableform(mock_response.selector)
    assert result == 2

def test_extract_dimensions_listform():
    spider = ListingSpider(asin="")
    mock_response = HtmlResponse(url='', body="""
        <div class="a-section table-padding">
            <table id="productDetails_detailBullets_sections1" class="a-keyvalue prodDetTable" role="presentation">
                <tr>
                    <th class="a-color-secondary a-size-base prodDetSectionEntry">ASIN</th>
                    <td class="a-size-base">B01N1037CV</td>
                </tr>
                <tr>
                    <th class="a-color-secondary a-size-base prodDetSectionEntry">Release date</th>
                    <td class="a-size-base">April 28, 2017</td>
                </tr>
                <tr>
                    <th class="a-color-secondary a-size-base prodDetSectionEntry">Best Sellers Rank</th>
                    <td><span>
                        <span>#21 in Video Games (<a href="">See Top 100 in Video Games</a>)</span>
                        <span>#4 in <a href="">Nintendo Switch Games</a></span>
                    </span></td>
                </tr>
                <tr>
                    <th class="a-color-secondary a-size-base prodDetSectionEntry">Pricing</th>
                    <td>
                        <span>The strikethrough price is the List Price. Savings represents a discount off the List Price.</span>
                    </td>
                </tr>
                <tr>
                    <th class="a-color-secondary a-size-base prodDetSectionEntry">Product Dimensions</th>
                    <td class="a-size-base">0.5 x 4.1 x 6.6 inches; 2.08 ounces</td>
                </tr>
                <tr>
                    <th class="a-color-secondary a-size-base prodDetSectionEntry">Media:</th>
                    <td class="a-size-base">Video Game</td>
                </tr>
            </table>
        </div>
    """, encoding='utf-8')
    result = spider.extract_dimensions_listform(mock_response.selector)
    assert result == '0.5 x 4.1 x 6.6 inches; 2.08 ounces'

def test_extract_rank_listform():
    spider = ListingSpider(asin="")
    mock_response = HtmlResponse(url='', body="""
        <div class="a-section table-padding">
            <table id="productDetails_detailBullets_sections1" class="a-keyvalue prodDetTable" role="presentation">
                <tr>
                    <th class="a-color-secondary a-size-base prodDetSectionEntry">ASIN</th>
                    <td class="a-size-base">B01N1037CV</td>
                </tr>
                <tr>
                    <th class="a-color-secondary a-size-base prodDetSectionEntry">Best Sellers Rank</th>
                    <td><span>
                        <span>#21 in Video Games (<a href="/gp/bestsellers/videogames/ref=pd_zg_ts_videogames">See Top 100 in Video Games</a>)</span>
                        <span>#4 in <a href="/gp/bestsellers/videogames/16227133011/ref=pd_zg_hrsr_videogames">Nintendo Switch Games</a></span>
                    </span></td>
                </tr>
                <tr>
                    <th class="a-color-secondary a-size-base prodDetSectionEntry">Pricing</th>
                    <td>
                        <span>The strikethrough price is the List Price. Savings represents a discount off the List Price.</span>
                    </td>
                </tr>
            </table>
        </div>
    """, encoding='utf-8')
    result = spider.extract_rank_listform(mock_response.selector)
    assert result == 4

def test_process_list():
    spider = ListingSpider(asin="B01MUAGZ49")
    mock_response = HtmlResponse(url='', body="""
        <div>
            <div id="wayfinding-breadcrumbs_container">
                <div id="wayfinding-breadcrumbs_feature_div">
                    <ul class="a-unordered-list a-horizontal a-size-small">
                        <li><span class="a-list-item"><a href="">Mock</a></span></li>
                        <li class="a-breadcrumb-divider"><span>›</span></li>
                        <li><span class="a-list-item"><a href="">List</a></span></li>
                        <li class="a-breadcrumb-divider"><span>›</span></li>
                        <li><span class="a-list-item"><a href="">Item</a></span></li>
                    </ul>
                </div>
            </div>
            <div class="a-section table-padding">
                <table id="productDetails_detailBullets_sections1" class="a-keyvalue prodDetTable" role="presentation">
                    <tr>
                        <th class="a-color-secondary a-size-base prodDetSectionEntry">Best Sellers Rank</th>
                        <td><span>
                            <span>#20 in Super Category (<a href=""></a>)</span>
                            <span>#1 in <a href="">Main Category</a></span>
                            <span>#3 in <a href="">Other Category</a></span>
                        </span></td>
                    </tr>
                    <tr>
                        <th class="a-color-secondary a-size-base prodDetSectionEntry">Product Dimensions</th>
                        <td class="a-size-base">3.0 x 4.1 x 5.0 inches</td>
                    </tr>
                </table>
            </div>
        </div>
    """, encoding='utf-8', request=Request(url="https://www.amazon.com/dp/B01MUAGZ49"))
    result = spider.process(mock_response)
    assert result['asin'] == "B01MUAGZ49"
    assert result['category'] == ["Mock", "List", "Item"]
    assert result['dimensions'] == "3.0 x 4.1 x 5.0 inches"
    assert result['rank'] == 1

def test_process_table():
    spider = ListingSpider(asin="B02GH1UY8P")
    mock_response = HtmlResponse(url='', body="""
        <div>
            <div id="wayfinding-breadcrumbs_container">
                <div id="wayfinding-breadcrumbs_feature_div">
                    <ul class="a-unordered-list a-horizontal a-size-small">
                        <li><span class="a-list-item"><a href="">Mock</a></span></li>
                        <li class="a-breadcrumb-divider"><span>›</span></li>
                        <li><span class="a-list-item"><a href="">Table</a></span></li>
                        <li class="a-breadcrumb-divider"><span>›</span></li>
                        <li><span class="a-list-item"><a href="">Item</a></span></li>
                    </ul>
                </div>
            </div>
            <div>
                <tbody>
                    <tr><td class="label">ASIN</td><td class="value">B002QYW8LW</td></tr>
                    <tr id="SalesRank">
                        <td class="label">Amazon Best Sellers Rank</td>
                        <td class="value">
                            #4000 in Broad Category (<a href=""></a>)
                            <ul class="zg_hrsr">
                                <li class="zg_hrsr_item">
                                    <span class="zg_hrsr_rank">#567</span>
                                    <span class="zg_hrsr_ladder">in <a href="">Specific Category</a></span>
                                </li>
                                <li class="zg_hrsr_item">
                                    <span class="zg_hrsr_rank">#2</span>
                                    <span class="zg_hrsr_ladder">in <a href="">Some other Category</a></span>
                                </li>
                            </ul>
                        </td>
                    </tr>
                    <tr class="shipping-weight">
                        <td class="label">Shipping Weight</td>
                        <td class="value">1.4 ounces (<a href="">View shipping rates and policies</a>)</td>
                    </tr>
                </tbody>
            </div>
                <div id="prodDetails">
                    <table cellspacing="0" cellpadding="0" border="0">
                        <tbody>
                            <tr class="size-weight"><td class="label">Item Weight</td><td class="value">5.5 lb</td></tr>
                            <tr class="size-weight"><td class="label">Product Dimensions</td><td class="value">1.2 x 0.4 x 5.6 cm</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    """, encoding='utf-8', request=Request(url="https://www.amazon.com/dp/B02GH1UY8P"))
    result = spider.process(mock_response)
    assert result['asin'] == "B02GH1UY8P"
    assert result['category'] == ["Mock", "Table", "Item"]
    assert result['dimensions'] == "1.2 x 0.4 x 5.6 cm"
    assert result['rank'] == 567
