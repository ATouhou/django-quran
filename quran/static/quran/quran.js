/**
 * Created by Mehmet on 6/12/2016.
 */

function remove_diacritics(input) {
    return input.replace(/[\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652\u0653\u0671\u0670\u06DC\u06DF\u06E0\u06E2\u06E3\u06E5\u06E6\u06E8\u06EA\u06EB\u06EC\u06ED]/g, '')
}

