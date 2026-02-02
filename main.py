#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neo4j Connector Plugin for Dify
Main entry point for the plugin
"""
from dify_plugin import Plugin, DifyPluginEnv

def main():
    """
    Initialize and start the Neo4j Connector plugin
    """
    # Create and start the plugin
    print("Starting Neo4j Connector Plugin...")
    print("Ready to connect to Neo4j databases")
    
    plugin = Plugin(DifyPluginEnv())
    plugin.run()


if __name__ == "__main__":
    main()
