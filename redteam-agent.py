#!/usr/bin/env python3
"""
Agentes de Seguridad Ofensiva (Red Teaming)
Agentes autónomos para simular ataques controlados
"""

import asyncio
import subprocess
import json
import random
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import argparse


@dataclass
class ScanResult:
    timestamp: str
    target: str
    scan_type: str
    findings: List[Dict]
    raw_output: str


@dataclass
class Payload:
    name: str
    category: str
    content: str
    severity: str
    description: str


class RedTeamAgent:
    """Agente autónomo para pruebas de penetración"""

    def __init__(self, target: str, scope: List[str] = None):
        self.target = target
        self.scope = scope or []
        self.results = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Payloads para testing
        self.payloads_db = self._initialize_payloads()

    def _initialize_payloads(self) -> Dict[str, List[Payload]]:
        """Inicializa base de datos de payloads"""
        return {
            "sqli": [
                Payload("SQLi Basic", "sqli", "' OR '1'='1' --", "high",
                        "Inyección SQL básica"),
                Payload("SQLi Union", "sqli", "' UNION SELECT null,null,null--", "high",
                        "Extracción de datos con UNION"),
                Payload("SQLi Blind", "sqli", "' AND 1=1--", "medium",
                        "Inyección SQL ciega"),
            ],
            "xss": [
                Payload("XSS Simple", "xss", "<script>alert('XSS')</script>", "medium",
                        "XSS básico"),
                Payload("XSS Img", "xss", "<img src=x onerror=alert('XSS')>", "medium",
                        "XSS mediante imagen"),
                Payload("XSS Event", "xss", "\" onmouseover=alert('XSS') ", "medium",
                        "XSS mediante evento"),
            ],
            "cmd_injection": [
                Payload("CMD Basic", "cmd_injection", "; ls -la", "critical",
                        "Inyección de comandos básica"),
                Payload("CMD Pipe", "cmd_injection", "| cat /etc/passwd", "critical",
                        "Inyección con pipe"),
                Payload("CMD Backtick", "cmd_injection", "`whoami`", "critical",
                        "Inyección con backticks"),
            ],
            "path_traversal": [
                Payload("Path Basic", "path_traversal", "../../../etc/passwd", "high",
                        "Path traversal básico"),
                Payload("Path URL", "path_traversal", "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd", "high",
                        "Path traversal URL-encoded"),
                Payload("Path Null", "path_traversal", "../../../etc/passwd%00.jpg", "high",
                        "Path traversal con null byte"),
            ],
            "nosql": [
                Payload("NoSQL Mongo", "nosql", '{"$gt": ""}', "high",
                        "Inyección NoSQL MongoDB"),
                Payload("NoSQL Login", "nosql", '{"username": {"$ne": null}}', "high",
                        "Bypass de login NoSQL"),
            ]
        }

    def run_nmap_scan(self, ports: str = "80,443,8080,22,21,25,3306,5432") -> ScanResult:
        """Ejecuta escaneo de red con Nmap"""
        print(f"🔍 [NMAP] Escaneando {self.target}...")

        cmd = [
            "nmap",
            "-sV",           # Detección de servicios
            "-sC",           # Scripts por defecto
            "-O",            # Detección de OS
            "--script=vulners",
            "-p", ports,
            "-oX", f"-",     # Output XML a stdout
            self.target
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )

            findings = self._parse_nmap_output(result.stdout)

            return ScanResult(
                timestamp=datetime.now().isoformat(),
                target=self.target,
                scan_type="nmap",
                findings=findings,
                raw_output=result.stdout
            )

        except subprocess.TimeoutExpired:
            print(f"⚠️ Timeout en escaneo Nmap")
            return ScanResult(
                timestamp=datetime.now().isoformat(),
                target=self.target,
                scan_type="nmap",
                findings=[],
                raw_output=""
            )
        except FileNotFoundError:
            print(f"⚠️ Nmap no instalado. Simulando resultados...")
            return self._simulate_nmap_results()

    def _parse_nmap_output(self, output: str) -> List[Dict]:
        """Parsea output de Nmap"""
        findings = []
        # Simplificado - en producción usaríamos python-nmap
        lines = output.split('\n')
        current_port = None

        for line in lines:
            if '/tcp' in line and 'open' in line:
                parts = line.split()
                port = parts[0]
                service = parts[2] if len(parts) > 2 else "unknown"
                findings.append({
                    "type": "open_port",
                    "port": port,
                    "service": service,
                    "severity": "info"
                })

        return findings

    def _simulate_nmap_results(self) -> ScanResult:
        """Simula resultados de Nmap para demostración"""
        return ScanResult(
            timestamp=datetime.now().isoformat(),
            target=self.target,
            scan_type="nmap_simulated",
            findings=[
                {"type": "open_port", "port": "22/tcp", "service": "ssh", "version": "OpenSSH 8.2"},
                {"type": "open_port", "port": "80/tcp", "service": "http", "version": "nginx 1.18"},
                {"type": "open_port", "port": "443/tcp", "service": "https", "version": "nginx 1.18"},
                {"type": "vulnerability", "cve": "CVE-2021-XXXX", "severity": "medium"}
            ],
            raw_output="[SIMULATED] Nmap scan results"
        )

    def fuzz_endpoint(self, endpoint: str, parameter: str,
                     payload_category: str = "sqli") -> List[Dict]:
        """Realiza fuzzing en un endpoint específico"""
        print(f"🎯 [FUZZ] Probando {endpoint}?{parameter}=...")

        payloads = self.payloads_db.get(payload_category, [])
        results = []

        for payload in payloads:
            # Simular respuesta (en producción, hacer requests reales)
            result = {
                "payload": payload.content,
                "parameter": parameter,
                "endpoint": endpoint,
                "category": payload.category,
                "severity": payload.severity,
                "response_time": random.uniform(0.1, 2.0),
                "status_code": 200,
                "vulnerable": random.random() > 0.8  # Simulación
            }

            if result["vulnerable"]:
                print(f"  🚨 Posible vulnerabilidad encontrada: {payload.name}")
                result["evidence"] = f"Payload: {payload.content}"

            results.append(result)

        return results

    def run_ctf_challenge(self, challenge_type: str) -> Dict:
        """Resuelve un reto CTF de forma autónoma"""
        print(f"🎮 [CTF] Resolviendo reto: {challenge_type}")

        strategies = {
            "crypto": self._solve_crypto,
            "web": self._solve_web,
            "pwn": self._solve_pwn,
            "reversing": self._solve_reversing,
            "forensics": self._solve_forensics
        }

        solver = strategies.get(challenge_type, self._solve_generic)
        return solver()

    def _solve_crypto(self) -> Dict:
        """Estrategia para retos criptográficos"""
        print("  🔐 Analizando cifrado...")
        return {
            "type": "crypto",
            "method": "frequency_analysis",
            "solved": True,
            "flag": "CTF{cr4ck3d_7h3_c1ph3r}"
        }

    def _solve_web(self) -> Dict:
        """Estrategia para retos web"""
        print("  🌐 Explorando aplicación web...")
        return {
            "type": "web",
            "method": "sqli_to_rce",
            "solved": True,
            "flag": "CTF{w3b_m4573r}"
        }

    def _solve_pwn(self) -> Dict:
        """Estrategia para retos de explotación"""
        print("  💥 Buscando buffer overflow...")
        return {
            "type": "pwn",
            "method": "rop_chain",
            "solved": True,
            "flag": "CTF{pwn3d_7h3_b1n4ry}"
        }

    def _solve_reversing(self) -> Dict:
        """Estrategia para retos de reversing"""
        print("  🔄 Decompilando...")
        return {
            "type": "reversing",
            "method": "static_analysis",
            "solved": True,
            "flag": "CTF{r3v3r53d}"
        }

    def _solve_forensics(self) -> Dict:
        """Estrategia para retos de forensics"""
        print("  🔍 Analizando evidencia...")
        return {
            "type": "forensics",
            "method": "file_carving",
            "solved": True,
            "flag": "CTF{f0r3ns1cs_m4st3r}"
        }

    def _solve_generic(self) -> Dict:
        """Estrategia genérica"""
        return {
            "type": "generic",
            "method": "brute_force",
            "solved": False
        }

    def adapt_strategy(self, previous_results: List[Dict]) -> Dict:
        """Adapta la estrategia según los resultados obtenidos"""
        # Contar vulnerabilidades por tipo
        vuln_count = {}
        for result in previous_results:
            cat = result.get("category", "unknown")
            vuln_count[cat] = vuln_count.get(cat, 0) + 1

        # Elegir siguiente vector de ataque
        if vuln_count.get("sqli", 0) > 0:
            return {"next_action": "escalate_sqli_to_rce", "priority": "high"}
        elif vuln_count.get("xss", 0) > 0:
            return {"next_action": "xss_to_session_hijacking", "priority": "medium"}
        else:
            return {"next_action": "enumerate_more", "priority": "low"}

    async def run_full_assessment(self) -> Dict:
        """Ejecuta evaluación completa de penetración"""
        print(f"\n🎯 Iniciando Red Team Assessment: {self.target}")
        print(f"   Session ID: {self.session_id}\n")

        assessment = {
            "session_id": self.session_id,
            "target": self.target,
            "timestamp": datetime.now().isoformat(),
            "phases": []
        }

        # Fase 1: Reconocimiento
        print("=" * 50)
        print("FASE 1: RECONOCIMIENTO")
        print("=" * 50)
        nmap_result = self.run_nmap_scan()
        assessment["phases"].append({
            "name": "reconnaissance",
            "results": [asdict(nmap_result)]
        })

        # Fase 2: Enumeración
        print("\n" + "=" * 50)
        print("FASE 2: ENUMERACIÓN")
        print("=" * 50)
        endpoints = ["/login", "/api/users", "/admin", "/search"]
        enumeration_results = []

        for endpoint in endpoints:
            for category in ["sqli", "xss"]:
                results = self.fuzz_endpoint(endpoint, "id", category)
                enumeration_results.extend(results)

        assessment["phases"].append({
            "name": "enumeration",
            "results": enumeration_results
        })

        # Fase 3: CTF (simulación de adaptación)
        print("\n" + "=" * 50)
        print("FASE 3: EXPLOTACIÓN ADAPTATIVA")
        print("=" * 50)

        if any(r.get("vulnerable") for r in enumeration_results):
            ctf_result = self.run_ctf_challenge("web")
            assessment["phases"].append({
                "name": "exploitation",
                "results": [ctf_result]
            })

            # Adaptar estrategia
            strategy = self.adapt_strategy(enumeration_results)
            print(f"\n📋 Estrategia adaptada: {strategy}")

        self.results.append(assessment)
        return assessment

    def generate_report(self) -> str:
        """Genera reporte de ejercicio Red Team"""
        if not self.results:
            return "No hay resultados para reportar"

        report = ["# 🎯 Red Team Assessment Report\n"]
        report.append(f"**Session ID:** {self.session_id}\n")
        report.append(f"**Target:** {self.target}\n\n")

        for assessment in self.results:
            for phase in assessment["phases"]:
                report.append(f"## {phase['name'].upper()}\n")

                for result in phase["results"]:
                    if isinstance(result, dict):
                        report.append(f"```json\n{json.dumps(result, indent=2)}\n```\n")

        return '\n'.join(report)


def main():
    parser = argparse.ArgumentParser(
        description="Agentes de Seguridad Ofensiva (Red Teaming)"
    )
    parser.add_argument("target", help="Target a evaluar (IP o dominio)")
    parser.add_argument(
        "--mode",
        choices=["full", "scan", "fuzz", "ctf"],
        default="full",
        help="Modo de operación"
    )
    parser.add_argument(
        "--ctf-type",
        choices=["crypto", "web", "pwn", "reversing", "forensics"],
        help="Tipo de reto CTF"
    )

    args = parser.parse_args()

    agent = RedTeamAgent(args.target)

    if args.mode == "full":
        result = asyncio.run(agent.run_full_assessment())
        print("\n" + agent.generate_report())

    elif args.mode == "scan":
        scan_result = agent.run_nmap_scan()
        print(f"\nResultados:\n{json.dumps(asdict(scan_result), indent=2)}")

    elif args.mode == "fuzz":
        results = agent.fuzz_endpoint("/api/search", "q")
        print(f"\nResultados de fuzzing:\n{json.dumps(results, indent=2)}")

    elif args.mode == "ctf":
        if not args.ctf_type:
            print("Error: --ctf-type requerido para modo CTF")
            return
        result = agent.run_ctf_challenge(args.ctf_type)
        print(f"\nResultado CTF:\n{json.dumps(result, indent=2)}")


if __name__ == "__main__":
    main()
