/**
 * Created by Mehmet on 6/12/2016.
 */

function remove_diacritics(input) {
    return input.replace(/[\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652\u0653\u0671\u0670\u06DC\u06DF\u06E0\u06E2\u06E3\u06E5\u06E6\u06E8\u06EA\u06EB\u06EC\u06ED]/g, '')
}

function arabic_numerals(input) {
    dic = {
        '0': '۰',
        '1': '١',
        '2': '٢',
        '3': '۳',
        '4': '۴',
        '5': '۵',
        '6': '۶',
        '7': '۷',
        '8': '۸',
        '9': '۹',
    }

    input = String(input)
    var output = ""

    var i = 0
    var max = input.length;
    while (i < max) {
        output += dic[input[i]]
        i++
    }

    return output
}

