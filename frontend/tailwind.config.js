/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',    // 蓝色 - 代表专注和生产力
        secondary: '#10B981',  // 绿色 - 代表完成和成就
        accent: '#F59E0B',     // 橙色 - 代表优先级和注意
        background: '#F3F4F6', // 浅灰 - 背景色
        text: '#1F2937',       // 深灰 - 文本色
        border: '#D1D5DB',     // 中灰 - 边框色
        success: '#10B981',    // 绿色 - 成功色
        error: '#EF4444',      // 红色 - 错误色
        warning: '#F59E0B',    // 黄色 - 警告色
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
