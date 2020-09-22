# -*- coding: utf-8 -*-

from mehdi_lib.basics import basic_types


dummy = basic_types.MultilingualString({
    basic_types.Language.AvailableLanguage.en: 'dummy',
    basic_types.Language.AvailableLanguage.fa: 'بیخودی',
})

file_path = basic_types.MultilingualString({
    basic_types.Language.AvailableLanguage.en: 'file path',
    basic_types.Language.AvailableLanguage.fa: 'مسیر فایل',
})

name = basic_types.MultilingualString({
    basic_types.Language.AvailableLanguage.en: 'name',
    basic_types.Language.AvailableLanguage.fa: 'نام',
})



