from typing import Any, Dict
from .schema import Component, Text, Button, Column, Row, Container, ForEach, Conditional, Binding
from .bindings import resolve_pointer

class CliRenderer:
    """
    Renders A2UI components to the terminal using rich formatting if available, 
    otherwise falls back to plain text.
    """
    def __init__(self, use_rich: bool = True):
        self.use_rich = use_rich
        if use_rich:
            try:
                from rich.console import Console
                from rich.panel import Panel
                from rich.table import Table
                from rich.live import Live
                from rich.progress import Progress, SpinnerColumn, TextColumn
                self.console = Console()
                self.Panel = Panel
                self.Table = Table
                self.Live = Live
                self.Progress = Progress
                self.SpinnerColumn = SpinnerColumn
                self.TextColumn = TextColumn
            except ImportError:
                self.use_rich = False

    def render(self, component: Component, context: Dict[str, Any]):
        """
        Main entry point for rendering a component tree to the CLI.
        """
        if not self.use_rich:
            print(self._render_plain(component, context))
            return

        # For rich rendering, we'll use a Panel or similar container
        self.console.print(self._render_rich(component, context))

    def _resolve(self, value: Any, context: Dict[str, Any]) -> Any:
        if isinstance(value, Binding):
            return resolve_pointer(context, value.bind, value.fallback)
        if isinstance(value, dict) and "bind" in value:
            return resolve_pointer(context, value["bind"], value.get("fallback"))
        return value

    def _render_plain(self, node: Any, context: Dict[str, Any]) -> str:
        if isinstance(node, Text):
            return str(self._resolve(node.content, context))
        elif isinstance(node, Column):
            return "\n".join([self._render_plain(c, context) for f in node.children])
        # ... fallback for other types
        return ""

    def _render_rich(self, node: Any, context: Dict[str, Any]) -> Any:
        from rich.text import Text as RichText
        from rich.console import Group
        
        if isinstance(node, Text):
            content = self._resolve(node.content, context)
            return RichText(str(content))
            
        elif isinstance(node, Column):
            children = [self._render_rich(child, context) for child in node.children]
            return Group(*children)
            
        elif isinstance(node, ForEach):
            items = self._resolve(node.items, context)
            if not isinstance(items, list): items = []
            children = []
            for item in items:
                child_ctx = context.copy()
                child_ctx[node.var] = item
                children.append(self._render_rich(node.template, child_ctx))
            return Group(*children)
            
        elif isinstance(node, Row):
            from rich.columns import Columns
            children = [self._render_rich(child, context) for child in node.children]
            return Columns(children)

        elif isinstance(node, Conditional):
            condition = self._resolve(node.condition, context)
            if condition:
                return self._render_rich(node.true_child, context)
            elif node.false_child:
                return self._render_rich(node.false_child, context)
            return RichText("")

        return RichText(f"[Unknown Component: {type(node).__name__}]", style="red")
