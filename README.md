# schedule
<!DOCTYPE html>
<html>
<head>
<style>
  :root { --aqua: #76D7EA; --pink: #F4C2C2; }
  body { font-family: 'Pretendard', sans-serif; background: transparent; margin: 0; padding: 10px; }
  .container { background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(10px); border-radius: 20px; overflow: hidden; border: 1px solid white; }
  .header { background: linear-gradient(135deg, var(--aqua), var(--pink)); color: white; padding: 15px; text-align: center; font-weight: bold; }
  table { width: 100%; border-collapse: collapse; table-layout: fixed; }
  th, td { padding: 10px 5px; text-align: center; border: 0.5px solid rgba(0,0,0,0.05); font-size: 12px; }
  .class-box { border-radius: 8px; padding: 5px; font-weight: 600; color: #444; font-size: 11px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
  .aqua { background: white; border-left: 4px solid var(--aqua); }
  .pink { background: white; border-left: 4px solid var(--pink); }
</style>
</head>
<body>
  <div class="container">
    <div class="header">🌊 NU AHOY: VOYAGE SCHEDULE ⚓</div>
    <table>
      <thead><tr><th>시간</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th></tr></thead>
      <tbody>
        {{CONTENT}}
      </tbody>
    </table>
  </div>
</body>
</html>
