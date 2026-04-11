"use client";

import { useEffect, useRef } from "react";

class Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  color: string;
  baseX: number;
  baseY: number;

  constructor(x: number, y: number) {
    this.x = x;
    this.y = y;
    this.baseX = x;
    this.baseY = y;
    this.vx = (Math.random() - 0.5) * 1;
    this.vy = (Math.random() - 0.5) * 1;
    this.radius = Math.random() * 2 + 1;

    const colors = ["#facc15", "#699cff", "#b95463"]; // Yellow, Blue, Purple/Red mix
    this.color = colors[Math.floor(Math.random() * colors.length)];
  }

  update(mouseX: number, mouseY: number, width: number, height: number) {
    // Wander around naturally
    this.baseX += this.vx;
    this.baseY += this.vy;

    // Bounce off edges smoothly
    if (this.baseX <= 0 || this.baseX >= width) this.vx *= -1;
    if (this.baseY <= 0 || this.baseY >= height) this.vy *= -1;

    // Lerp towards mouse loosely
    let targetX = this.baseX;
    let targetY = this.baseY;

    if (mouseX !== -1 && mouseY !== -1) {
      const dx = mouseX - this.baseX;
      const dy = mouseY - this.baseY;
      const dist = Math.sqrt(dx * dx + dy * dy);

      if (dist < 400) {
        // Move slightly towards cursor
        targetX += dx * 0.05 * (400 - dist) / 400;
        targetY += dy * 0.05 * (400 - dist) / 400;
      }
    }

    // Smooth integration
    this.x += (targetX - this.x) * 0.05;
    this.y += (targetY - this.y) * 0.05;
  }

  draw(ctx: CanvasRenderingContext2D) {
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
    ctx.fillStyle = this.color;
    ctx.globalAlpha = 0.4;
    ctx.shadowBlur = 15;
    ctx.shadowColor = this.color;
    ctx.fill();
    ctx.globalAlpha = 1.0;
    ctx.shadowBlur = 0;
  }
}

export function BubbleBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animationFrameId: number;
    let particles: Particle[] = [];
    let mouseX = -1;
    let mouseY = -1;

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      initParticles();
    };

    const initParticles = () => {
      particles = [];
      const numParticles = Math.min(Math.floor((window.innerWidth * window.innerHeight) / 15000), 100);
      for (let i = 0; i < numParticles; i++) {
        particles.push(
          new Particle(
            Math.random() * canvas.width,
            Math.random() * canvas.height
          )
        );
      }
    };

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      particles.forEach((p) => {
        p.update(mouseX, mouseY, canvas.width, canvas.height);
        p.draw(ctx);
      });

      animationFrameId = requestAnimationFrame(animate);
    };

    const handleMouseMove = (e: MouseEvent) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    };

    const handleMouseLeave = () => {
      mouseX = -1;
      mouseY = -1;
    };

    window.addEventListener("resize", resize);
    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseleave", handleMouseLeave);

    resize();
    animate();

    return () => {
      window.removeEventListener("resize", resize);
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseleave", handleMouseLeave);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none w-full h-full z-0 opacity-80"
    />
  );
}
