"use client";

import { useEffect, useRef } from "react";

interface Blob {
  x: number; y: number;
  vx: number; vy: number;
  radius: number;
  color: string;
  alpha: number;
}

export function BubbleBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let raf: number;
    let blobs: Blob[] = [];
    let mouseX = -1, mouseY = -1;

    // Accent colors from design system
    const colors = [
      "#facc15", // yellow accent
      "#4f8ef7", // blue
      "#8b5cf6", // purple
      "#22d3ee", // cyan
    ];

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      init();
    };

    const init = () => {
      blobs = [];
      const count = Math.min(Math.floor((window.innerWidth * window.innerHeight) / 20000), 80);
      for (let i = 0; i < count; i++) {
        blobs.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          vx: (Math.random() - 0.5) * 0.6,
          vy: (Math.random() - 0.5) * 0.6,
          radius: Math.random() * 1.8 + 0.8,
          color: colors[Math.floor(Math.random() * colors.length)],
          alpha: Math.random() * 0.35 + 0.1,
        });
      }
    };

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      for (const b of blobs) {
        // drift
        b.x += b.vx;
        b.y += b.vy;

        // bounce
        if (b.x < 0 || b.x > canvas.width) b.vx *= -1;
        if (b.y < 0 || b.y > canvas.height) b.vy *= -1;

        // attract toward mouse gently
        if (mouseX !== -1) {
          const dx = mouseX - b.x;
          const dy = mouseY - b.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 300) {
            const force = (300 - dist) / 300 * 0.03;
            b.x += dx * force;
            b.y += dy * force;
          }
        }

        ctx.beginPath();
        ctx.arc(b.x, b.y, b.radius, 0, Math.PI * 2);
        ctx.fillStyle = b.color;
        ctx.globalAlpha = b.alpha;
        ctx.shadowBlur = 12;
        ctx.shadowColor = b.color;
        ctx.fill();
        ctx.globalAlpha = 1;
        ctx.shadowBlur = 0;
      }

      // Draw subtle connecting lines between nearby particles
      for (let i = 0; i < blobs.length; i++) {
        for (let j = i + 1; j < blobs.length; j++) {
          const dx = blobs[i].x - blobs[j].x;
          const dy = blobs[i].y - blobs[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 120) {
            const alpha = (1 - dist / 120) * 0.06;
            ctx.beginPath();
            ctx.moveTo(blobs[i].x, blobs[i].y);
            ctx.lineTo(blobs[j].x, blobs[j].y);
            ctx.strokeStyle = `rgba(250, 204, 21, ${alpha})`;
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        }
      }

      raf = requestAnimationFrame(animate);
    };

    const onMouseMove = (e: MouseEvent) => { mouseX = e.clientX; mouseY = e.clientY; };
    const onMouseLeave = () => { mouseX = -1; mouseY = -1; };

    window.addEventListener("resize", resize);
    window.addEventListener("mousemove", onMouseMove);
    window.addEventListener("mouseleave", onMouseLeave);

    resize();
    animate();

    return () => {
      window.removeEventListener("resize", resize);
      window.removeEventListener("mousemove", onMouseMove);
      window.removeEventListener("mouseleave", onMouseLeave);
      cancelAnimationFrame(raf);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none w-full h-full z-0"
      style={{ opacity: 0.7 }}
    />
  );
}
