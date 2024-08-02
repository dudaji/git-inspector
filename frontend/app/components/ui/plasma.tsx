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
      animationDuration: `${Math.random() * 0.5 + 5}s`, // random animation speed
      animationDelay: `${Math.random() * 5}s`,
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