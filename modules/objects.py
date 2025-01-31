from modules.types import Filter

xpaths: dict = {
    'wg-card': '//div[contains(@class, "wgg_card") and contains(@class, "offer_list_item")]',
    'save-cookies': '//*[@id="cmpwelcomebtnsave"]/a',
    'more-options': '//a[@class="show_more_filters"]',
    'apply-filters': '//button[contains(@class, "filter_submit_button") and contains(@class, "wgg_blue")]',
    'dropdown-menu': '//ul[contains(@class, "dropdown-menu") and contains(@class, "inner")]',
    'date-picker': '[div@id="ui-datepicker-div"]',
    'select-year': '//select[@data-handler="selectYear"]',
    'select-month': '//select[@data-handler="selectMonth"]',
    'date-calendar': '//table[@class="ui-datepicker-calendar"]',
    Filter.RentType.value: '//button[@title="All Rent Types"]',
    Filter.EarliestMove.value: '//input[@id="date_from_input"]',
    Filter.Searched.value: '//button[@data-id="wgSea"]',
}

filters: dict[Filter, str] = {
    Filter.RentType.value: 'Long Term,Short Term',
    Filter.EarliestMove.value: '01.April.2025',
    Filter.Searched.value: 'Male/s',
    Filter.WithPhotos.value: 'True',
}
