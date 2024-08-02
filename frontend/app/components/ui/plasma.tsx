// components/ui/PlasmaEffect.tsx
const generateLightningPath = (width: number, height: number, segments: number) => {
  let path = `M0 ${height / 2}`;
  for (let i = 1; i <= segments; i++) {
    const x = (width / segments) * i;
    const y = Math.random() * height;
    path += ` L${x} ${y}`;
  }
  return path;
};

const generateRandomLightning = (count: number) => {
  return Array.from({ length: count }, (_, i) => {
    const width = Math.random() * 50 + 10; // plasma width
    const height = Math.random() * 50 + 10; // plasma height
    const segments = Math.floor(Math.random() * 5) + 7; // 3-7 segments
    return {
      top: `${Math.random() * 100}%`,
      left: `${Math.random() * 100}%`,
      width: `${width}%`,
      height: `${height}%`,
      path: generateLightningPath(width, height, segments),
      animationDuration: `${Math.random() * 10}s`, // 0초에서 10초 사이
      animationDelay: `${Math.random() * 10}s`, // 0초에서 10초 사이
    };
  });
};

export const PlasmaEffect = () => {
  const lightnings = generateRandomLightning(7); // n개의 랜덤한 plasma 생성

  return (
    <div className="plasma-effect absolute inset-0 pointer-events-none overflow-hidden">
      {lightnings.map((lightning, index) => (
        <svg
          key={index}
          className="absolute"
          style={{
            top: lightning.top,
            left: lightning.left,
            width: lightning.width,
            height: lightning.height,
          }}
        >
          <path
            d={lightning.path}
            className="plasma-line"
            fill="none"
            strokeLinecap="round"
            strokeLinejoin="round"
            style={{
              animationDuration: lightning.animationDuration,
              animationDelay: lightning.animationDelay,
            }}
          />
        </svg>
      ))}
    </div>
  );
};

/* Guide for plasma

width = Math.random() * 50 + 10: 플라즈마의 너비 (10%에서 60% 사이)
height = Math.random() * 50 + 10: 플라즈마의 높이 (10%에서 60% 사이)
segments = Math.floor(Math.random() * 5) + 7: 플라즈마 선의 굴곡 수 (7에서 11 사이)
top: ${Math.random() * 100}%: 플라즈마의 수직 위치 (0%에서 100% 사이)
left: ${Math.random() * 100}%: 플라즈마의 수평 위치 (0%에서 100% 사이)
animationDuration: ${Math.random() * 0.5 + 5}s: 애니메이션 속도 (5초에서 5.5초 사이)
animationDelay: ${Math.random() * 5}s: 애니메이션 시작 지연 시간 (0초에서 5초 사이)
generateRandomLightning(7): 생성할 플라즈마의 수

이 값들을 조정하여 원하는 효과를 얻을 수 있습니다. 예를 들어:

더 빠른 애니메이션을 원한다면 animationDuration을 줄이세요.
더 많은 플라즈마를 원한다면 generateRandomLightning()의 인자를 늘리세요.
더 복잡한 형태의 플라즈마를 원한다면 segments의 범위를 늘리세요.
더 강한 빛 효과를 원한다면 CSS의 stroke 투명도와 drop-shadow 값을 조정하세요.

*/