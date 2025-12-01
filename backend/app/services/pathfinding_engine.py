"""
Maritime Pathfinding Engine
Multi-algorithm pathfinding implementation for maritime route optimization.

Algorithms:
- Dijkstra's algorithm for optimal cost routes
- A* with nautical heuristics for time-optimized routes
- Hub-based routing for global shipping lane optimization
- Custom maritime algorithms for reliability optimization
"""

import heapq
import math
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

import structlog

from app.models.maritime import Port, Coordinates, VesselConstraints, OptimizationCriteria
from app.utils.maritime_calculations import calculate_great_circle_distance

logger = structlog.get_logger(__name__)


@dataclass
class PathNode:
    """Represents a node in the pathfinding graph."""
    port: Port
    g_cost: float  # Cost from start to this node
    h_cost: float  # Heuristic cost estimate to destination
    f_cost: float  # Total estimated cost (g + h)
    parent: Optional['PathNode'] = None
    
    def __lt__(self, other: 'PathNode') -> bool:
        return self.f_cost < other.f_cost
    
    def __eq__(self, other: 'PathNode') -> bool:
        return self.port.unlocode == other.port.unlocode


class PathfindingEngine:
    """
    Enterprise-grade pathfinding engine for maritime route optimization.
    
    Implements multiple pathfinding algorithms optimized for maritime
    routing with vessel constraints and real-time factor integration.
    
    Performance targets:
    - Simple routes: <200ms pathfinding
    - Complex multi-hop: <1s pathfinding
    - Memory efficient for global port networks
    """
    
    def __init__(self):
        # Graph representation of shipping network
        self._shipping_graph: Dict[str, Dict[str, float]] = {}
        self._port_lookup: Dict[str, Port] = {}
        
        # Performance tracking
        self.stats = {
            "dijkstra_calls": 0,
            "astar_calls": 0,
            "hub_routing_calls": 0,
            "average_path_length": 0.0
        }
        
        # Major shipping hubs for hub-based routing
        self._major_hubs = {
            "SGSIN", "NLRTM", "CNSHA", "AEJEA", "USLAX",
            "DEHAM", "HKHKG", "USPNY", "BEANR", "JPNGO"
        }
    
    def build_graph(self, ports: List[Port], max_edge_distance_nm: float = 5000.0) -> None:
        """
        Build shipping network graph from port list.
        
        Creates edges between ports within feasible sailing distance,
        optimizing for realistic maritime routing patterns.
        
        Args:
            ports: List of ports to include in graph
            max_edge_distance_nm: Maximum distance for direct edges
        """
        start_time = datetime.utcnow()
        
        # Clear existing graph
        self._shipping_graph.clear()
        self._port_lookup.clear()
        
        # Index ports by code
        for port in ports:
            self._port_lookup[port.unlocode] = port
            self._shipping_graph[port.unlocode] = {}
        
        # Build edges between ports
        edges_created = 0
        for i, port1 in enumerate(ports):
            for port2 in ports[i + 1:]:
                distance = calculate_great_circle_distance(
                    port1.coordinates, port2.coordinates
                )
                
                if distance <= max_edge_distance_nm:
                    # Bidirectional edges
                    self._shipping_graph[port1.unlocode][port2.unlocode] = distance
                    self._shipping_graph[port2.unlocode][port1.unlocode] = distance
                    edges_created += 1
        
        build_duration = (datetime.utcnow() - start_time).total_seconds()
        
        logger.info(
            "Shipping graph built",
            ports=len(ports),
            edges=edges_created,
            duration_seconds=round(build_duration, 3)
        )
    
    def dijkstra(
        self,
        origin_code: str,
        destination_code: str,
        vessel_constraints: Optional[VesselConstraints] = None
    ) -> Optional[List[str]]:
        """
        Find shortest path using Dijkstra's algorithm.
        
        Optimal for cost-based routing where we want the minimum
        total edge weight (distance/cost) path.
        
        Args:
            origin_code: Starting port UN/LOCODE
            destination_code: Ending port UN/LOCODE
            vessel_constraints: Optional vessel constraints for filtering
            
        Returns:
            List of port codes representing optimal path, or None if no path
        """
        self.stats["dijkstra_calls"] += 1
        start_time = datetime.utcnow()
        
        if origin_code not in self._shipping_graph:
            logger.warning(f"Origin port {origin_code} not in graph")
            return None
        
        if destination_code not in self._shipping_graph:
            logger.warning(f"Destination port {destination_code} not in graph")
            return None
        
        # Initialize distances and visited set
        distances: Dict[str, float] = {origin_code: 0}
        previous: Dict[str, Optional[str]] = {origin_code: None}
        visited: Set[str] = set()
        
        # Priority queue: (distance, port_code)
        pq: List[Tuple[float, str]] = [(0, origin_code)]
        
        while pq:
            current_dist, current_port = heapq.heappop(pq)
            
            if current_port in visited:
                continue
            
            visited.add(current_port)
            
            # Found destination
            if current_port == destination_code:
                path = self._reconstruct_path(previous, destination_code)
                duration = (datetime.utcnow() - start_time).total_seconds()
                
                logger.debug(
                    "Dijkstra path found",
                    origin=origin_code,
                    destination=destination_code,
                    path_length=len(path),
                    total_distance=round(current_dist, 2),
                    duration_ms=round(duration * 1000, 2)
                )
                
                return path
            
            # Explore neighbors
            for neighbor, edge_distance in self._shipping_graph[current_port].items():
                if neighbor in visited:
                    continue
                
                # Apply vessel constraints if provided
                if vessel_constraints and not self._is_edge_feasible(
                    current_port, neighbor, vessel_constraints
                ):
                    continue
                
                new_distance = current_dist + edge_distance
                
                if neighbor not in distances or new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_port
                    heapq.heappush(pq, (new_distance, neighbor))
        
        logger.warning(
            "No path found (Dijkstra)",
            origin=origin_code,
            destination=destination_code
        )
        return None
    
    def astar(
        self,
        origin_code: str,
        destination_code: str,
        vessel_constraints: Optional[VesselConstraints] = None
    ) -> Optional[List[str]]:
        """
        Find shortest path using A* algorithm with nautical heuristics.
        
        Uses great circle distance as admissible heuristic for faster
        convergence on time-optimized routing.
        
        Args:
            origin_code: Starting port UN/LOCODE
            destination_code: Ending port UN/LOCODE
            vessel_constraints: Optional vessel constraints for filtering
            
        Returns:
            List of port codes representing optimal path, or None if no path
        """
        self.stats["astar_calls"] += 1
        start_time = datetime.utcnow()
        
        if origin_code not in self._port_lookup:
            logger.warning(f"Origin port {origin_code} not in graph")
            return None
        
        if destination_code not in self._port_lookup:
            logger.warning(f"Destination port {destination_code} not in graph")
            return None
        
        origin_port = self._port_lookup[origin_code]
        destination_port = self._port_lookup[destination_code]
        
        # Initialize with origin node
        origin_node = PathNode(
            port=origin_port,
            g_cost=0,
            h_cost=self._heuristic(origin_port, destination_port),
            f_cost=0
        )
        origin_node.f_cost = origin_node.h_cost
        
        # Open set (priority queue) and closed set
        open_set: List[PathNode] = [origin_node]
        open_set_codes: Set[str] = {origin_code}
        closed_set: Set[str] = set()
        
        # Best g_cost for each node
        g_costs: Dict[str, float] = {origin_code: 0}
        
        while open_set:
            current = heapq.heappop(open_set)
            open_set_codes.discard(current.port.unlocode)
            
            # Found destination
            if current.port.unlocode == destination_code:
                path = self._reconstruct_astar_path(current)
                duration = (datetime.utcnow() - start_time).total_seconds()
                
                logger.debug(
                    "A* path found",
                    origin=origin_code,
                    destination=destination_code,
                    path_length=len(path),
                    total_cost=round(current.g_cost, 2),
                    duration_ms=round(duration * 1000, 2)
                )
                
                return path
            
            closed_set.add(current.port.unlocode)
            
            # Explore neighbors
            for neighbor_code, edge_distance in self._shipping_graph.get(
                current.port.unlocode, {}
            ).items():
                if neighbor_code in closed_set:
                    continue
                
                neighbor_port = self._port_lookup.get(neighbor_code)
                if not neighbor_port:
                    continue
                
                # Apply vessel constraints
                if vessel_constraints and not self._is_edge_feasible(
                    current.port.unlocode, neighbor_code, vessel_constraints
                ):
                    continue
                
                tentative_g = current.g_cost + edge_distance
                
                if neighbor_code not in g_costs or tentative_g < g_costs[neighbor_code]:
                    g_costs[neighbor_code] = tentative_g
                    h_cost = self._heuristic(neighbor_port, destination_port)
                    
                    neighbor_node = PathNode(
                        port=neighbor_port,
                        g_cost=tentative_g,
                        h_cost=h_cost,
                        f_cost=tentative_g + h_cost,
                        parent=current
                    )
                    
                    if neighbor_code not in open_set_codes:
                        heapq.heappush(open_set, neighbor_node)
                        open_set_codes.add(neighbor_code)
        
        logger.warning(
            "No path found (A*)",
            origin=origin_code,
            destination=destination_code
        )
        return None
    
    def hub_based_routing(
        self,
        origin_code: str,
        destination_code: str,
        vessel_constraints: Optional[VesselConstraints] = None,
        max_hubs: int = 2
    ) -> Optional[List[str]]:
        """
        Find route through strategic shipping hubs.
        
        Identifies optimal paths that utilize major transshipment hubs,
        which often provide more reliable and cost-effective routing.
        
        Args:
            origin_code: Starting port UN/LOCODE
            destination_code: Ending port UN/LOCODE
            vessel_constraints: Optional vessel constraints
            max_hubs: Maximum number of hub stops
            
        Returns:
            List of port codes representing hub-based path
        """
        self.stats["hub_routing_calls"] += 1
        
        if origin_code not in self._port_lookup:
            return None
        if destination_code not in self._port_lookup:
            return None
        
        origin_port = self._port_lookup[origin_code]
        destination_port = self._port_lookup[destination_code]
        
        # Find nearest hubs to origin and destination
        origin_hubs = self._find_nearest_hubs(origin_port, 3)
        destination_hubs = self._find_nearest_hubs(destination_port, 3)
        
        best_path: Optional[List[str]] = None
        best_distance = float('inf')
        
        # Try direct path first
        direct_path = self.astar(origin_code, destination_code, vessel_constraints)
        if direct_path:
            direct_distance = self._calculate_path_distance(direct_path)
            best_path = direct_path
            best_distance = direct_distance
        
        # Try single hub routing
        for hub_code in origin_hubs.union(destination_hubs):
            if hub_code == origin_code or hub_code == destination_code:
                continue
            
            # Path: origin -> hub -> destination
            path1 = self.dijkstra(origin_code, hub_code, vessel_constraints)
            path2 = self.dijkstra(hub_code, destination_code, vessel_constraints)
            
            if path1 and path2:
                combined_path = path1 + path2[1:]  # Avoid duplicate hub
                total_distance = self._calculate_path_distance(combined_path)
                
                # Accept if within 20% of direct distance or shorter
                if total_distance < best_distance * 1.2:
                    if total_distance < best_distance:
                        best_path = combined_path
                        best_distance = total_distance
        
        # Try two-hub routing if max_hubs >= 2
        if max_hubs >= 2:
            for hub1 in origin_hubs:
                for hub2 in destination_hubs:
                    if hub1 == hub2 or hub1 == origin_code or hub2 == destination_code:
                        continue
                    
                    path1 = self.dijkstra(origin_code, hub1, vessel_constraints)
                    path2 = self.dijkstra(hub1, hub2, vessel_constraints)
                    path3 = self.dijkstra(hub2, destination_code, vessel_constraints)
                    
                    if path1 and path2 and path3:
                        combined_path = path1 + path2[1:] + path3[1:]
                        total_distance = self._calculate_path_distance(combined_path)
                        
                        if total_distance < best_distance:
                            best_path = combined_path
                            best_distance = total_distance
        
        if best_path:
            logger.debug(
                "Hub-based route found",
                origin=origin_code,
                destination=destination_code,
                path_length=len(best_path),
                total_distance=round(best_distance, 2)
            )
        
        return best_path
    
    def find_alternative_paths(
        self,
        origin_code: str,
        destination_code: str,
        vessel_constraints: Optional[VesselConstraints] = None,
        num_alternatives: int = 3
    ) -> List[List[str]]:
        """
        Find multiple alternative paths between ports.
        
        Uses penalty method to discourage reuse of edges from
        previously found paths, generating diverse route options.
        
        Args:
            origin_code: Starting port UN/LOCODE
            destination_code: Ending port UN/LOCODE
            vessel_constraints: Optional vessel constraints
            num_alternatives: Number of alternatives to find
            
        Returns:
            List of alternative paths
        """
        alternatives: List[List[str]] = []
        used_edges: Set[Tuple[str, str]] = set()
        
        for i in range(num_alternatives):
            # Find path avoiding used edges
            path = self._find_path_avoiding_edges(
                origin_code, destination_code, used_edges, vessel_constraints
            )
            
            if path and path not in alternatives:
                alternatives.append(path)
                
                # Add edges to used set
                for j in range(len(path) - 1):
                    used_edges.add((path[j], path[j + 1]))
                    used_edges.add((path[j + 1], path[j]))
        
        return alternatives
    
    def _heuristic(self, port: Port, destination: Port) -> float:
        """
        Calculate admissible heuristic (great circle distance).
        
        Args:
            port: Current port
            destination: Destination port
            
        Returns:
            Heuristic distance estimate
        """
        return calculate_great_circle_distance(
            port.coordinates, destination.coordinates
        )
    
    def _reconstruct_path(
        self, 
        previous: Dict[str, Optional[str]], 
        destination: str
    ) -> List[str]:
        """Reconstruct path from previous pointers (Dijkstra)."""
        path = []
        current: Optional[str] = destination
        
        while current is not None:
            path.append(current)
            current = previous.get(current)
        
        path.reverse()
        return path
    
    def _reconstruct_astar_path(self, node: PathNode) -> List[str]:
        """Reconstruct path from A* node chain."""
        path = []
        current: Optional[PathNode] = node
        
        while current is not None:
            path.append(current.port.unlocode)
            current = current.parent
        
        path.reverse()
        return path
    
    def _is_edge_feasible(
        self,
        from_code: str,
        to_code: str,
        vessel_constraints: VesselConstraints
    ) -> bool:
        """
        Check if edge is feasible given vessel constraints.
        
        Args:
            from_code: Origin port code
            to_code: Destination port code
            vessel_constraints: Vessel constraints
            
        Returns:
            True if edge is feasible for vessel
        """
        # Check vessel range
        distance = self._shipping_graph.get(from_code, {}).get(to_code, float('inf'))
        if distance > vessel_constraints.max_range_nautical_miles:
            return False
        
        # Check port compatibility
        destination_port = self._port_lookup.get(to_code)
        if destination_port:
            if not destination_port.is_compatible_with_vessel(
                vessel_constraints.length_meters,
                vessel_constraints.beam_meters,
                vessel_constraints.draft_meters
            ):
                return False
        
        return True
    
    def _find_nearest_hubs(self, port: Port, count: int) -> Set[str]:
        """Find nearest major shipping hubs to a port."""
        hub_distances: List[Tuple[float, str]] = []
        
        for hub_code in self._major_hubs:
            hub_port = self._port_lookup.get(hub_code)
            if hub_port:
                distance = calculate_great_circle_distance(
                    port.coordinates, hub_port.coordinates
                )
                hub_distances.append((distance, hub_code))
        
        hub_distances.sort()
        return {code for _, code in hub_distances[:count]}
    
    def _calculate_path_distance(self, path: List[str]) -> float:
        """Calculate total distance of a path."""
        total = 0.0
        for i in range(len(path) - 1):
            total += self._shipping_graph.get(path[i], {}).get(path[i + 1], 0)
        return total
    
    def _find_path_avoiding_edges(
        self,
        origin_code: str,
        destination_code: str,
        avoid_edges: Set[Tuple[str, str]],
        vessel_constraints: Optional[VesselConstraints]
    ) -> Optional[List[str]]:
        """
        Find path while avoiding specified edges.
        
        Uses penalty method to discourage but not completely prohibit
        use of specified edges.
        """
        # Create modified graph with penalties
        penalty_factor = 2.0
        
        if origin_code not in self._shipping_graph:
            return None
        
        distances: Dict[str, float] = {origin_code: 0}
        previous: Dict[str, Optional[str]] = {origin_code: None}
        visited: Set[str] = set()
        
        pq: List[Tuple[float, str]] = [(0, origin_code)]
        
        while pq:
            current_dist, current_port = heapq.heappop(pq)
            
            if current_port in visited:
                continue
            
            visited.add(current_port)
            
            if current_port == destination_code:
                return self._reconstruct_path(previous, destination_code)
            
            for neighbor, base_distance in self._shipping_graph[current_port].items():
                if neighbor in visited:
                    continue
                
                # Apply penalty for avoided edges
                edge = (current_port, neighbor)
                edge_distance = base_distance
                if edge in avoid_edges:
                    edge_distance *= penalty_factor
                
                if vessel_constraints and not self._is_edge_feasible(
                    current_port, neighbor, vessel_constraints
                ):
                    continue
                
                new_distance = current_dist + edge_distance
                
                if neighbor not in distances or new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_port
                    heapq.heappush(pq, (new_distance, neighbor))
        
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get pathfinding statistics."""
        return {
            **self.stats,
            "graph_nodes": len(self._shipping_graph),
            "total_edges": sum(len(edges) for edges in self._shipping_graph.values()) // 2
        }
