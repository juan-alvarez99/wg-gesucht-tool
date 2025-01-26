xpaths: dict[str, str] = {
    'wg-card': '//div[contains(@class, "wgg_card") and contains(@class, "offer_list_item")]',
    'save-cookies': '//*[@id="cmpwelcomebtnsave"]/a',
    'more-options': '//a[@class="show_more_filters"]',
    'apply-filters': '//button[contains(@class, "filter_submit_button") and contains(@class, "wgg_blue")]',
    'rent-type': '//button[@title="All Rent Types"]',
    'dropdown-menu': '//ul[contains(@class, "dropdown-menu") and contains(@class, "inner")]'
}

filters: dict[str, str] = {
    'rent-type': 'Long Term,Short Term',
    'earliest-move': '1.4.2025',
    'searched': 'male',
    'my-age': '25',
    'with-photos': 'True',
}