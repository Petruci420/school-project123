"""
PC Specs Requirements Checker Module

This module evaluates if user hardware can run a specific game based on 
minimum and recommended requirements.

Usage:
    from pc_specs_checker import check_game_compatibility
    
    result = check_game_compatibility(
        user_hardware={...},
        game_requirements={...}
    )
"""

import json
from typing import Dict, Any

# Placeholder benchmark database for CPU scores
# Higher score = better performance
CPU_BENCHMARK_DB = {
    # Intel CPUs
    "Intel Core i9-13900K": 45000,
    "Intel Core i7-13700K": 38000,
    "Intel Core i5-13600K": 32000,
    "Intel Core i9-12900K": 40000,
    "Intel Core i7-12700K": 35000,
    "Intel Core i5-12600K": 28000,
    "Intel Core i7-11700K": 25000,
    "Intel Core i5-11600K": 20000,
    "Intel Core i7-10700K": 22000,
    "Intel Core i5-10400": 15000,
    "Intel Core i3-10100": 10000,
    # AMD CPUs
    "AMD Ryzen 9 7950X": 48000,
    "AMD Ryzen 9 7900X": 42000,
    "AMD Ryzen 7 7700X": 35000,
    "AMD Ryzen 5 7600X": 28000,
    "AMD Ryzen 9 5950X": 38000,
    "AMD Ryzen 9 5900X": 35000,
    "AMD Ryzen 7 5800X": 28000,
    "AMD Ryzen 5 5600X": 22000,
    "AMD Ryzen 7 3700X": 20000,
    "AMD Ryzen 5 3600": 16000,
    "AMD Ryzen 3 3300X": 12000,
}

# Placeholder benchmark database for GPU scores
# Higher score = better performance (based on approximate 3DMark scores)
GPU_BENCHMARK_DB = {
    # NVIDIA RTX 40 Series
    "NVIDIA GeForce RTX 4090": 35000,
    "NVIDIA GeForce RTX 4080": 28000,
    "NVIDIA GeForce RTX 4070 Ti": 24000,
    "NVIDIA GeForce RTX 4070": 20000,
    "NVIDIA GeForce RTX 4060 Ti": 16000,
    "NVIDIA GeForce RTX 4060": 14000,
    # NVIDIA RTX 30 Series
    "NVIDIA GeForce RTX 3090": 25000,
    "NVIDIA GeForce RTX 3080": 22000,
    "NVIDIA GeForce RTX 3070": 18000,
    "NVIDIA GeForce RTX 3060 Ti": 15000,
    "NVIDIA GeForce RTX 3060": 13000,
    "NVIDIA GeForce RTX 3050": 10000,
    # NVIDIA GTX 16 Series
    "NVIDIA GeForce GTX 1660 Ti": 9000,
    "NVIDIA GeForce GTX 1660": 8000,
    "NVIDIA GeForce GTX 1650": 6000,
    # AMD RX 7000 Series
    "AMD Radeon RX 7900 XTX": 30000,
    "AMD Radeon RX 7900 XT": 26000,
    "AMD Radeon RX 7800 XT": 22000,
    "AMD Radeon RX 7700 XT": 18000,
    "AMD Radeon RX 7600": 14000,
    # AMD RX 6000 Series
    "AMD Radeon RX 6900 XT": 23000,
    "AMD Radeon RX 6800 XT": 20000,
    "AMD Radeon RX 6700 XT": 16000,
    "AMD Radeon RX 6600 XT": 12000,
    "AMD Radeon RX 6600": 10000,
    "AMD Radeon RX 6500 XT": 7000,
}


def get_cpu_score(cpu_name: str, cores: int = None, clock_speed: float = None) -> int:
    """
    Get benchmark score for a CPU.
    
    Args:
        cpu_name: Name of the CPU (e.g., "Intel Core i7-13700K")
        cores: Number of cores (optional, for estimation if CPU not in DB)
        clock_speed: Clock speed in GHz (optional, for estimation)
    
    Returns:
        Benchmark score (integer)
    """
    # Check if CPU exists in database
    if cpu_name in CPU_BENCHMARK_DB:
        return CPU_BENCHMARK_DB[cpu_name]
    
    # Fallback: estimate based on cores and clock speed if provided
    if cores and clock_speed:
        # Simple estimation formula (not accurate, just for placeholder)
        estimated_score = int(cores * clock_speed * 1000)
        return estimated_score
    
    # Default fallback for unknown CPUs
    return 10000


def get_gpu_score(gpu_name: str, vram_gb: int = None) -> int:
    """
    Get benchmark score for a GPU.
    
    Args:
        gpu_name: Name of the GPU (e.g., "NVIDIA GeForce RTX 3060")
        vram_gb: VRAM in GB (optional, for basic filtering)
    
    Returns:
        Benchmark score (integer)
    """
    # Check if GPU exists in database
    if gpu_name in GPU_BENCHMARK_DB:
        return GPU_BENCHMARK_DB[gpu_name]
    
    # Fallback: rough estimation based on VRAM if provided
    if vram_gb:
        # Rough estimation (not accurate)
        if vram_gb >= 16:
            return 20000
        elif vram_gb >= 12:
            return 15000
        elif vram_gb >= 8:
            return 12000
        elif vram_gb >= 6:
            return 9000
        elif vram_gb >= 4:
            return 6000
        else:
            return 3000
    
    # Default fallback for unknown GPUs
    return 8000


def check_game_compatibility(user_hardware: Dict[str, Any], game_requirements: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check if user hardware can run a game based on requirements.
    
    Args:
        user_hardware: Dictionary with user hardware specs
            {
                "cpu": {
                    "name": str,
                    "cores": int (optional),
                    "clock_speed": float (optional, in GHz),
                    "score": int (optional, if already known)
                },
                "gpu": {
                    "name": str,
                    "vram_gb": int,
                    "score": int (optional, if already known)
                },
                "ram_gb": int
            }
        
        game_requirements: Dictionary with game requirements
            {
                "minimum": {
                    "cpu_score": int,
                    "gpu_score": int,
                    "ram_gb": int
                },
                "recommended": {
                    "cpu_score": int,
                    "gpu_score": int,
                    "ram_gb": int
                }
            }
    
    Returns:
        Dictionary with compatibility result:
            {
                "can_run": bool (True/False),
                "settings": str ("Cannot Run", "Low", "Medium", "High"),
                "notes": str (explanation),
                "details": {
                    "cpu_meets_min": bool,
                    "cpu_meets_rec": bool,
                    "gpu_meets_min": bool,
                    "gpu_meets_rec": bool,
                    "ram_meets_min": bool,
                    "ram_meets_rec": bool
                }
            }
    """
    
    # Step 1: Extract user hardware scores
    user_cpu_score = user_hardware["cpu"].get("score")
    if user_cpu_score is None:
        user_cpu_score = get_cpu_score(
            user_hardware["cpu"]["name"],
            user_hardware["cpu"].get("cores"),
            user_hardware["cpu"].get("clock_speed")
        )
    
    user_gpu_score = user_hardware["gpu"].get("score")
    if user_gpu_score is None:
        user_gpu_score = get_gpu_score(
            user_hardware["gpu"]["name"],
            user_hardware["gpu"].get("vram_gb")
        )
    
    user_ram_gb = user_hardware["ram_gb"]
    
    # Step 2: Get game requirements
    min_reqs = game_requirements["minimum"]
    rec_reqs = game_requirements["recommended"]
    
    # Step 3: Check minimum requirements
    cpu_meets_min = user_cpu_score >= min_reqs["cpu_score"]
    gpu_meets_min = user_gpu_score >= min_reqs["gpu_score"]
    ram_meets_min = user_ram_gb >= min_reqs["ram_gb"]
    
    # Step 4: Check recommended requirements
    cpu_meets_rec = user_cpu_score >= rec_reqs["cpu_score"]
    gpu_meets_rec = user_gpu_score >= rec_reqs["gpu_score"]
    ram_meets_rec = user_ram_gb >= rec_reqs["ram_gb"]
    
    # Step 5: Determine if game can run
    meets_minimum = cpu_meets_min and gpu_meets_min and ram_meets_min
    meets_recommended = cpu_meets_rec and gpu_meets_rec and ram_meets_rec
    
    # Step 6: Generate result
    if not meets_minimum:
        # Cannot run at all
        bottlenecks = []
        if not cpu_meets_min:
            bottlenecks.append(f"CPU (yours: {user_cpu_score}, need: {min_reqs['cpu_score']})")
        if not gpu_meets_min:
            bottlenecks.append(f"GPU (yours: {user_gpu_score}, need: {min_reqs['gpu_score']})")
        if not ram_meets_min:
            bottlenecks.append(f"RAM (yours: {user_ram_gb}GB, need: {min_reqs['ram_gb']}GB)")
        
        return {
            "can_run": False,
            "settings": "Cannot Run",
            "notes": f"Hardware below minimum requirements. Bottlenecks: {', '.join(bottlenecks)}",
            "details": {
                "cpu_meets_min": cpu_meets_min,
                "cpu_meets_rec": cpu_meets_rec,
                "gpu_meets_min": gpu_meets_min,
                "gpu_meets_rec": gpu_meets_rec,
                "ram_meets_min": ram_meets_min,
                "ram_meets_rec": ram_meets_rec,
                "user_scores": {
                    "cpu": user_cpu_score,
                    "gpu": user_gpu_score,
                    "ram": user_ram_gb
                }
            }
        }
    
    elif meets_recommended:
        # Can run on HIGH settings
        return {
            "can_run": True,
            "settings": "High",
            "notes": "Your hardware meets or exceeds recommended requirements. Enjoy high settings!",
            "details": {
                "cpu_meets_min": cpu_meets_min,
                "cpu_meets_rec": cpu_meets_rec,
                "gpu_meets_min": gpu_meets_min,
                "gpu_meets_rec": gpu_meets_rec,
                "ram_meets_min": ram_meets_min,
                "ram_meets_rec": ram_meets_rec,
                "user_scores": {
                    "cpu": user_cpu_score,
                    "gpu": user_gpu_score,
                    "ram": user_ram_gb
                }
            }
        }
    
    else:
        # Can run but not at recommended (LOW/MEDIUM settings)
        # Determine LOW vs MEDIUM based on how close to recommended
        cpu_gap = (user_cpu_score - min_reqs["cpu_score"]) / (rec_reqs["cpu_score"] - min_reqs["cpu_score"])
        gpu_gap = (user_gpu_score - min_reqs["gpu_score"]) / (rec_reqs["gpu_score"] - min_reqs["gpu_score"])
        ram_gap = (user_ram_gb - min_reqs["ram_gb"]) / (rec_reqs["ram_gb"] - min_reqs["ram_gb"])
        
        # Average gap to determine setting tier
        avg_gap = (cpu_gap + gpu_gap + ram_gap) / 3
        
        if avg_gap >= 0.5:
            settings = "Medium"
            notes = "Your hardware is between minimum and recommended. Expect medium settings."
        else:
            settings = "Low"
            notes = "Your hardware meets minimum requirements. Expect low settings for smooth gameplay."
        
        return {
            "can_run": True,
            "settings": settings,
            "notes": notes,
            "details": {
                "cpu_meets_min": cpu_meets_min,
                "cpu_meets_rec": cpu_meets_rec,
                "gpu_meets_min": gpu_meets_min,
                "gpu_meets_rec": gpu_meets_rec,
                "ram_meets_min": ram_meets_min,
                "ram_meets_rec": ram_meets_rec,
                "user_scores": {
                    "cpu": user_cpu_score,
                    "gpu": user_gpu_score,
                    "ram": user_ram_gb
                }
            }
        }


# Example usage (for testing)
if __name__ == "__main__":
    # Example user hardware
    user_hw = {
        "cpu": {
            "name": "AMD Ryzen 5 5600X",
            "cores": 6,
            "clock_speed": 3.7
        },
        "gpu": {
            "name": "NVIDIA GeForce RTX 3060",
            "vram_gb": 12
        },
        "ram_gb": 16
    }
    
    # Example game requirements (e.g., Cyberpunk 2077)
    game_reqs = {
        "minimum": {
            "cpu_score": 16000,
            "gpu_score": 9000,
            "ram_gb": 8
        },
        "recommended": {
            "cpu_score": 25000,
            "gpu_score": 18000,
            "ram_gb": 16
        }
    }
    
    result = check_game_compatibility(user_hw, game_reqs)
    print(json.dumps(result, indent=2))
