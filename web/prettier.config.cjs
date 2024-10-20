/** @type {import("prettier").Config} */
module.exports = {
  trailingComma: 'es5',
  tabWidth: 2,
  semi: false,
  singleQuote: true,
  endOfLine: 'auto',
  plugins: [require.resolve('prettier-plugin-tailwindcss')],
}
