(function() {
  var style = getComputedStyle(document.documentElement);
  var accent = style.getPropertyValue('--accent').trim();
  var accent2 = style.getPropertyValue('--accent2').trim();
  var ink = style.getPropertyValue('--ink').trim();
  var muted = style.getPropertyValue('--muted').trim();
  var rule = style.getPropertyValue('--rule').trim();
  var bg2 = style.getPropertyValue('--bg2').trim();

  var commonGrid = {
    left: '3%',
    right: '4%',
    bottom: '3%',
    top: '12%',
    containLabel: true
  };

  var commonTooltip = {
    trigger: 'axis',
    backgroundColor: bg2,
    borderColor: rule,
    textStyle: { color: ink }
  };

  var categoryAxis = {
    type: 'category',
    axisLine: { lineStyle: { color: rule } },
    axisLabel: { color: muted, fontSize: 11 },
    axisTick: { show: false }
  };

  var valueAxis = {
    type: 'value',
    splitLine: { lineStyle: { color: rule, type: 'dashed' } },
    axisLabel: { color: muted, fontSize: 11 }
  };

  function initBar(id, title, data, horizontal) {
    var el = document.getElementById(id);
    if (!el) return;
    var chart = echarts.init(el, null, { renderer: 'svg' });

    var names = data.map(function(d) { return d[0]; });
    var values = data.map(function(d) { return d[1]; });

    var option = {
      animation: false,
      tooltip: commonTooltip,
      grid: {
        left: horizontal ? '22%' : '3%',
        right: '4%',
        bottom: horizontal ? '3%' : '8%',
        top: '8%',
        containLabel: true
      },
      xAxis: horizontal ? categoryAxis : valueAxis,
      yAxis: horizontal ? valueAxis : categoryAxis,
      series: [{
        type: 'bar',
        data: horizontal ? values : values.reverse(),
        itemStyle: {
          color: accent,
          borderRadius: horizontal ? [0, 4, 4, 0] : [4, 4, 0, 0]
        },
        label: {
          show: true,
          position: horizontal ? 'right' : 'top',
          color: muted,
          fontSize: 10
        }
      }]
    };

    if (horizontal) {
      option.xAxis.data = names;
    } else {
      option.yAxis.data = names.reverse();
    }

    chart.setOption(option);
    window.addEventListener('resize', function() { chart.resize(); });
  }

  function initPie(id, data) {
    var el = document.getElementById(id);
    if (!el) return;
    var chart = echarts.init(el, null, { renderer: 'svg' });
    var option = {
      animation: false,
      tooltip: {
        trigger: 'item',
        backgroundColor: bg2,
        borderColor: rule,
        textStyle: { color: ink },
        formatter: '{b}: {c} ({d}%)'
      },
      legend: {
        bottom: 0,
        textStyle: { color: muted, fontSize: 11 }
      },
      series: [{
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['50%', '45%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 6,
          borderColor: bg2,
          borderWidth: 2
        },
        label: {
          show: false
        },
        data: data,
        color: [accent, accent2, muted]
      }]
    };
    chart.setOption(option);
    window.addEventListener('resize', function() { chart.resize(); });
  }

  // Platform distribution
  initPie('chart-platform', [
    { value: 311, name: 'Website' },
    { value: 17, name: 'App' }
  ]);

  // Tier distribution
  initPie('chart-tier', [
    { value: 214, name: 'Premium' },
    { value: 114, name: '免费' }
  ]);

  // Categories
  initBar('chart-categories', 'Top 10 页面分类', [
    ['Landing Page', 60],
    ['Hero', 57],
    ['Hero Section', 34],
    ['SaaS', 28],
    ['Agency', 9],
    ['Features', 8],
    ['CTA', 8],
    ['About', 6],
    ['Pricing', 6],
    ['Portfolio', 5]
  ], true);

  // Tech stack
  initBar('chart-tech', '核心技术栈', [
    ['React', 276],
    ['Tailwind CSS', 266],
    ['Vite', 182],
    ['TypeScript', 176],
    ['Lucide Icons', 157],
    ['Framer Motion', 70],
    ['Figma', 33],
    ['GSAP', 17],
    ['shadcn/ui', 15],
    ['Next.js', 4]
  ], true);

  // Motion types
  initBar('chart-motion', '动效类型', [
    ['过渡 transition', 1138],
    ['缩放 scale', 984],
    ['淡入淡出 fade', 951],
    ['动画 animate', 797],
    ['缓动 ease', 666],
    ['滑动 slide', 402],
    ['错开 stagger', 319],
    ['旋转 rotate', 308],
    ['弹性 spring', 52],
    ['入场 entrance', 31]
  ], true);

  // Components
  initBar('chart-components', '页面组件', [
    ['CTA', 505],
    ['Footer 页脚', 336],
    ['Navbar 导航栏', 300],
    ['Pricing 定价', 250],
    ['Stats 数据展示', 236],
    ['About 关于', 212],
    ['Hero 首屏', 183],
    ['Marquee 跑马灯', 170],
    ['Navigation 导航', 145],
    ['Accordion 手风琴', 137]
  ], true);

  // Luxury terms
  initBar('chart-luxury', '高级感描述词频', [
    ['bold 大胆', 218],
    ['cinematic 电影感', 53],
    ['modern 现代', 41],
    ['clean 干净', 30],
    ['high-end 高端', 16],
    ['minimal 极简', 13],
    ['immersive 沉浸', 11],
    ['stunning 惊艳', 10],
    ['professional 专业', 9],
    ['editorial 编辑式', 7]
  ], true);
})();
