import { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Sphere, Line } from '@react-three/drei';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import * as THREE from 'three';

function WaterMolecule() {
  const groupRef = useRef<THREE.Group>(null);

  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = state.clock.getElapsedTime() * 0.3;
    }
  });

  const oxygenPos: [number, number, number] = [0, 0, 0];
  const hydrogen1Pos: [number, number, number] = [-1.5, -0.8, 0];
  const hydrogen2Pos: [number, number, number] = [1.5, -0.8, 0];

  return (
    <group ref={groupRef}>
      <Sphere position={oxygenPos} args={[0.5, 32, 32]}>
        <meshStandardMaterial color="red" />
      </Sphere>
      
      <Sphere position={hydrogen1Pos} args={[0.3, 32, 32]}>
        <meshStandardMaterial color="white" />
      </Sphere>
      
      <Sphere position={hydrogen2Pos} args={[0.3, 32, 32]}>
        <meshStandardMaterial color="white" />
      </Sphere>

      <Line
        points={[oxygenPos, hydrogen1Pos]}
        color="gray"
        lineWidth={3}
      />
      <Line
        points={[oxygenPos, hydrogen2Pos]}
        color="gray"
        lineWidth={3}
      />
    </group>
  );
}

export default function ARLesson() {
  return (
    <div className="container mx-auto p-6 space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="text-3xl">AR/VR Molecular Visualization</CardTitle>
          <div className="flex gap-2 mt-2">
            <Badge>Biology</Badge>
            <Badge variant="outline">Advanced</Badge>
          </div>
        </CardHeader>
        <CardContent>
          <div className="w-full h-[500px] bg-gray-900 rounded-lg overflow-hidden">
            <Canvas camera={{ position: [0, 0, 8], fov: 50 }}>
              <ambientLight intensity={0.5} />
              <pointLight position={[10, 10, 10]} intensity={1} />
              <pointLight position={[-10, -10, -10]} intensity={0.5} />
              <WaterMolecule />
              <OrbitControls enableZoom={true} enablePan={true} />
            </Canvas>
          </div>

          <div className="mt-4 space-y-2">
            <h3 className="font-semibold text-lg">Interactive 3D Water Molecule (H₂O)</h3>
            <p className="text-sm text-gray-600">
              Use your mouse to rotate, zoom, and explore the molecular structure. 
              The red sphere represents oxygen (O) and the white spheres represent hydrogen (H) atoms.
            </p>
            <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
              <li>Left-click and drag to rotate the molecule</li>
              <li>Scroll to zoom in and out</li>
              <li>Right-click and drag to pan the view</li>
            </ul>
          </div>

          <div className="mt-4 space-y-2">
            <h3 className="font-semibold text-lg">Coming Soon:</h3>
            <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
              <li>DNA double helix visualization</li>
              <li>AR/VR immersive mode for mobile devices</li>
              <li>AlphaFold protein structure integration</li>
              <li>Real-time molecular dynamics simulations</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
