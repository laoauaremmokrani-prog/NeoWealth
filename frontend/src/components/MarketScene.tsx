
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Stars, Float } from '@react-three/drei';
import { useRef } from 'react';
import * as THREE from 'three';

function Candle({ position, color, height }: { position: [number, number, number], color: string, height: number }) {
    const meshRef = useRef<THREE.Mesh>(null);

    useFrame((state) => {
        if (meshRef.current) {
            meshRef.current.rotation.y += 0.01;
            // Gentle floating
            meshRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime + position[0]) * 0.2;
        }
    });

    return (
        <Float speed={2} rotationIntensity={0.5} floatIntensity={0.5}>
            <mesh ref={meshRef} position={position}>
                <boxGeometry args={[0.4, height, 0.4]} />
                <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.5} transparent opacity={0.8} />
            </mesh>
        </Float>
    );
}

function MarketGraph() {
    const points = [];
    const count = 20;

    for (let i = 0; i < count; i++) {
        const isUp = Math.random() > 0.4;
        const color = isUp ? '#00ffa3' : '#ff4d4d';
        const height = Math.random() * 3 + 1;
        const x = (i - count / 2) * 0.6;
        points.push(<Candle key={i} position={[x, 0, 0]} color={color} height={height} />);
    }

    return <group>{points}</group>;
}

export default function MarketScene() {
    return (
        <div className="scene-wrapper">
            <Canvas camera={{ position: [0, 2, 12], fov: 45 }}>
                <color attach="background" args={['#050510']} />
                <ambientLight intensity={0.5} />
                <pointLight position={[10, 10, 10]} intensity={1} />
                <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />

                <MarketGraph />

                <OrbitControls enableZoom={false} autoRotate autoRotateSpeed={0.5} />
                <gridHelper args={[20, 20, '#1a1a1a', '#111']} position={[0, -2, 0]} />
            </Canvas>
        </div>
    );
}
