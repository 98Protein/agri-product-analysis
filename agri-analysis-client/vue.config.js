/*
 * @Author: liangtd
 * @Date: 2023-05-30 14:42:17
 * @LastEditors: liangtd
 * @LastEditTime: 2023-05-30 18:02:29
 * @Description: 
 */
module.exports = {
  devServer: {
    host: 'localhost',
    port: 8080,
    proxy: {
        '/api': {
            target: 'http://192.168.216.128:5050',
            changeOrigin: true,
            ws: true,
            pathRewrite: {
              '^/api': ''
            }
        }
    }
  }
}