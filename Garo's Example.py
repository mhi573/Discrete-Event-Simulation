import simpy
import random
import pandas as pd
from datetime import datetime, timedelta
import networkx as nx
import matplotlib.pyplot as plt

# Define the Restaurant class
class Restaurant:
    def __init__(self, env):
        # Initialize the Restaurant class with the environment and resources
        self.env = env
        # Resources for waitstaff A and B
        self.waitstaff_A = simpy.Resource(env, capacity=1)
        self.waitstaff_B = simpy.Resource(env, capacity=1)
        # Log to store the simulation events
        self.log = []

    # Methods to simulate different activities
    def seat_guest(self, order_number, server):
        # Simulate seating a guest
        yield self.env.timeout(random.randint(1, 3))
        # Log the event
        self.log.append([self.env.now, order_number, 'Seated', server])

    def visit_table(self, order_number, server):
        # Simulate visiting a table
        yield self.env.timeout(random.randint(2, 5))
        # Log the event
        self.log.append([self.env.now, order_number, 'Visit Table', server])

    def post_order(self, order_number, server):
        # Simulate posting an order
        yield self.env.timeout(random.randint(1, 3))
        # Log the event
        self.log.append([self.env.now, order_number, 'Order Posted', server])

    def deliver_order(self, order_number, server):
        # Simulate delivering an order
        yield self.env.timeout(random.randint(5, 10))
        # Log the event
        self.log.append([self.env.now, order_number, 'Order Delivered', server])

    def deliver_bill(self, order_number, server):
        # Simulate delivering a bill
        yield self.env.timeout(random.randint(1, 2))
        # Log the event
        self.log.append([self.env.now, order_number, 'Bill Delivered', server])

    def pay_bill(self, order_number, server):
        # Simulate paying a bill
        yield self.env.timeout(random.randint(1, 3))
        # Log the event
        self.log.append([self.env.now, order_number, 'Bill Paid', server])

    def process_order(self, order_number):
        # Process an order using resources and simulation of activities
        with self.waitstaff_A.request() as request:
            yield request
            # Sequence of activities for processing an order
            yield self.env.process(self.seat_guest(order_number, 'Waitstaff A'))
            yield self.env.process(self.visit_table(order_number, 'Waitstaff A'))
            yield self.env.process(self.post_order(order_number, 'Waitstaff A'))
            yield self.env.process(self.deliver_order(order_number, 'Waitstaff A'))
            yield self.env.process(self.deliver_bill(order_number, 'Waitstaff A'))
            yield self.env.process(self.pay_bill(order_number, 'Waitstaff A'))

# Run the simulation and create the process graph
def run_simulation_with_analysis():
    # Create the simulation environment
    env = simpy.Environment()
    # Initialize the restaurant
    restaurant = Restaurant(env)
    # Simulate processing multiple orders
    for i in range(10):  # Simulate 10 orders
        env.process(restaurant.process_order(i))
    # Run the simulation until a specific time
    env.run(until=100)

    # Convert log to DataFrame and format timestamps
    df = pd.DataFrame(restaurant.log, columns=['Time', 'Order Number', 'Activity', 'Server'])
    df['Time'] = df['Time'].astype(int)  # Convert time to int for minutes
    df['Date Time'] = df['Time'].apply(lambda x: datetime(2024, 5, 26, 16, 0) + timedelta(minutes=x))
    df = df[['Date Time', 'Order Number', 'Activity', 'Server']]

    # Calculate metrics
    activity_times = df.groupby('Activity')['Date Time'].agg(['min', 'max'])
    activity_times['Duration'] = (activity_times['max'] - activity_times['min']).dt.total_seconds() / 60
    activity_times.drop(columns=['min', 'max'], inplace=True)
    order_times = df.groupby('Order Number')['Date Time'].agg(['min', 'max'])
    order_times['Duration'] = (order_times['max'] - order_times['min']).dt.total_seconds() / 60
    order_times.drop(columns=['min', 'max'], inplace=True)
    avg_order_time = order_times['Duration'].mean()

    # Print statistical analysis
    print("\nStatistical Analysis:")
    print("Average Time to Complete Each Activity (in minutes):")
    print(activity_times)
    print("\nTotal Time Spent per Order (in minutes):")
    print(order_times)
    print("\nAverage Time Spent per Order (in minutes):", avg_order_time)

    # Create the table with the desired format
    print("\nActivity Log Table:")
    print(df.to_string(index=False))

    return df

# Create a process graph
def create_process_graph(df):
    # Create a directed graph
    G = nx.DiGraph()
    
    # Add nodes and edges based on the activities
    activities = df['Activity'].unique()
    for i in range(len(activities) - 1):
        G.add_edge(activities[i], activities[i + 1])
    
    # Draw the graph
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=12, font_weight="bold", arrowsize=20)
    plt.title("Restaurant Process Flow")
    plt.show()

# Run the simulation with analysis
df_log = run_simulation_with_analysis()

# Create the process graph
create_process_graph(df_log)
