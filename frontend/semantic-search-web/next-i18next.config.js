/**
 * Because next-i18next has some problem, so keep its as a .js file
 *
 * dont try to change it to .mjs/.mts/.ts file unless you can make sure it working nice
 */

const crc32 = require('crc').crc32
const path = require('path')

/** @type {import('next-i18next').UserConfig} */
module.exports = {
  // debug: process.env.NODE_ENV === 'development',
  i18n: {
    defaultLocale: 'en',
    locales: [
      'en',
      'zh-CN',
      'de-DE',
      'es-ES',
      'fr-FR',
      'ja-JP',
      'pt-BR',
      'ru-RU',
    ],
    localeDetection: false,
  },
  serializeConfig: false,
  defaultNS: 'translation',
  reloadOnPrerender: process.env.NODE_ENV === 'development',
  localePath: path.resolve('./public/locales'),
  // onPreInitI18next: (_i18n) => {
  // not work in server side
  // replace by custom useTranslation
  // const originT = i18n.t
  // i18n.t = (key, defaultValue, options) => {
  //   try {
  //     const hashKey = `k${crc32(key).toString(16)}`
  //     let words = originT(hashKey, defaultValue, options)
  //     if (words === hashKey) {
  //       words = key
  //       console.info(`[i18n] miss translation: [${hashKey}] ${key}`)
  //     }
  //     return words
  //   } catch (err) {
  //     console.error(err)
  //     return key
  //   }
  // }
  // },
  react: {
    transSupportBasicHtmlNodes: false,
    hashTransKey(defaultValue) {
      // return a key based on defaultValue or if you prefer to just remind you should set a key return false and throw an error
      return `k${crc32(defaultValue).toString(16)}`
    },
  },
}
