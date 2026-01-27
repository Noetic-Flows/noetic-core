import asyncio
import argparse
import os
import json
import sys

# Ensure project packages are in path for plain python3 usage
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
for pkg in ["lang-python", "knowledge-python", "stage-python", "conscience-python", "engine-python"]:
    pkg_path = os.path.join(base_dir, "packages", pkg)
    if pkg_path not in sys.path:
        sys.path.insert(0, pkg_path)

# Also inject virtual environment site-packages if not already present
# This allows plain system python to find installed dependencies
venv_site = os.path.join(base_dir, ".venv311/lib/python3.11/site-packages")
if os.path.exists(venv_site) and venv_site not in sys.path:
    sys.path.append(venv_site)

from noetic_engine.runtime.engine import NoeticEngine
from noetic_engine.loader import NoeticLoader
from noetic_lang.core import IdentityContext

async def main():
    parser = argparse.ArgumentParser(description="Noetic CLI Reference Implementation")
    parser.add_argument("--codex", type=str, help="Path to the .noetic Codex file")
    parser.add_argument("--query", type=str, default="What is Software 3.0?", help="Initial query")
    args = parser.parse_args()

    print("--- Noetic CLI Agent ---")
    
    # 1. Initialize Engine
    engine = NoeticEngine(db_url="sqlite:///noetic_cli.db")
    
    # 2. Setup Identity
    identity = IdentityContext(
        user_id="user.cli",
        roles=["admin"]
    )
    
    # 3. Load Codex
    loader = NoeticLoader()
    codex_path = args.codex
    if not codex_path:
        codex_path = os.path.abspath("apps/python-cli/cli_default.noetic")
        if not os.path.exists(codex_path):
            print("Creating default CLI codex...")
            default_codex = {
                "id": "codex.cli.default",
                "orchestration": {
                    "agents": [
                        {
                            "id": "agent.researcher",
                            "system_prompt": "You are a research agent.",
                            "allowed_skills": ["skill.debug.log"],
                            "principles": []
                        }
                    ],
                    "flows": [
                        {
                            "id": "flow.main",
                            "start_at": "Research",
                            "states": {
                                "Research": {
                                    "type": "Task",
                                    "description": "Searching the web for current knowledge",
                                    "skill": "skill.debug.log",
                                    "params": {"message": "Processing Query..."},
                                    "end": True
                                }
                            }
                        }
                    ]
                }
            }
            with open(codex_path, "w") as f:
                json.dump(default_codex, f, indent=2)

    loader.load(engine, codex_path)
    
    # Override the message if using default flow to be dynamic
    if not args.codex:
        executor = engine.flow_manager.get_executor("flow.main")
        if executor and "Research" in executor.flow_model.states:
            executor.flow_model.states["Research"].description = f"Researching: {args.query}"
            executor.flow_model.states["Research"].params["message"] = f"Starting research on {args.query}"

    # 4. Start Engine (Run in background task)
    engine_task = asyncio.create_task(engine.start())
    
    from noetic_stage.cli_renderer import CliRenderer
    from rich.live import Live
    from rich.panel import Panel
    from rich.console import Group
    from rich.text import Text as RichText
    
    cli_renderer = CliRenderer()
    
    try:
        # 5. Trigger Flow
        print(f"Triggering Flow with query: {args.query}")
        engine.push_event("cmd.run_flow", {
            "flow_id": "flow.main",
            "identity": identity.model_dump(),
            "query": args.query
        })
        
        # 6. Real-time Live Display
        with Live(RichText("Initializing..."), refresh_per_second=4, console=cli_renderer.console) as live:
            max_retries = 20
            for i in range(max_retries):
                await asyncio.sleep(0.5)
                
                # Get World State
                state = engine.knowledge.get_world_state()
                
                # Build a display group
                display_items = []
                
                # 1. Current Goal
                goals = [f for f in state.facts if f.predicate == "current_goal"]
                if goals:
                    display_items.append(Panel(RichText(f"🎯 {goals[-1].object_literal}", style="bold cyan"), title="Current Goal", border_style="cyan"))
                
                # 2. Activity Feed (used_skill facts)
                usage = [f for f in state.facts if f.predicate == "used_skill"]
                if usage:
                    activity = Group(*[RichText(f"✔️ {f.object_literal}", style="green") for f in usage])
                    display_items.append(Panel(activity, title="Executed Steps", border_style="blue"))
                
                # 3. Cognitive Progress
                if usage:
                    progress_text = RichText(f"🚀 Processing... Completed {len(usage)} actions.", style="yellow")
                    display_items.append(progress_text)
                
                if display_items:
                    live.update(Panel(Group(*display_items), title="[bold]Noetic Agent Status[/bold]", subtitle=f"Query: {args.query}"))
                
                if len(usage) >= 1 and i > 5:
                    break 
        
        print("\n--- Execution Complete ---")
            
    finally:
        await engine.stop()
        engine_task.cancel()
        try:
            await engine_task
        except asyncio.CancelledError:
            pass
        print("\n--- CLI Agent Stopped ---")

if __name__ == "__main__":
    asyncio.run(main())
