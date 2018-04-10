package dk.itu.mario.engine.level.generator;

import java.util.*;
import java.util.ArrayList;
import java.util.Random;

import dk.itu.mario.MarioInterface.Constraints;
import dk.itu.mario.MarioInterface.GamePlay;
import dk.itu.mario.MarioInterface.LevelGenerator;
import dk.itu.mario.MarioInterface.LevelInterface;
import dk.itu.mario.engine.level.Level;
import dk.itu.mario.engine.level.MyLevel;
import dk.itu.mario.engine.level.MyDNA;

import dk.itu.mario.engine.PlayerProfile;

import dk.itu.mario.engine.sprites.SpriteTemplate;
import dk.itu.mario.engine.sprites.Enemy;

//Yuen Han Chan
public class MyLevelGenerator{
	
	public boolean verbose = true; //print debugging info
	
	// MAKE ANY NEW MEMBER VARIABLES HERE
	
	// Called by the game engine.
	// Returns the level to be played.
	public Level generateLevel(PlayerProfile playerProfile)
	{
		// Call genetic algorithm to optimize to the player profile
		MyDNA dna = this.geneticAlgorithm(playerProfile);
		
		// Post process
		dna = this.postProcess(dna);
		
		// Convert the solution to the GA into a Level
		MyLevel level = new MyLevel(dna, LevelInterface.TYPE_OVERGROUND);
		
		return (Level)level;
	}
	
	// Genetic Algorithm implementation
	private MyDNA geneticAlgorithm (PlayerProfile playerProfile)
	{
		// Set the population size
		int populationSize = getPopulationSize();
		
		// Make the population array
		ArrayList<MyDNA> population = new ArrayList<MyDNA>();
		
		// Make the solution, which is initially null
		MyDNA solution = null;
		
		// Generate a random population
		for (int i=0; i < populationSize; i++) {
			MyDNA newIndividual = this.generateRandomIndividual();
			newIndividual.setFitness(this.evaluateFitness(newIndividual, playerProfile));
			population.add(newIndividual);
		}
		if (this.verbose) {
			System.out.println("Initial population:");
			printPopulation(population);
		}
		
		// Iteration counter
		int count = 0;
		
		// Iterate until termination criteria met
		while (!this.terminate(population, count)) {
			// Make a new, possibly larger population
			System.out.println("i am at count: " + count);
			ArrayList<MyDNA> newPopulation = new ArrayList<MyDNA>();

			// Keep track of individual's parents (for this iteration only)
			Hashtable parents = new Hashtable();

			// Mutuate a number of individuals
			ArrayList<MyDNA> mutationPool = this.selectIndividualsForMutation(population);
			for (int i=0; i < mutationPool.size(); i++) {
				MyDNA parent = mutationPool.get(i);
				// Mutate
				MyDNA mutant = parent.mutate();
				// Evaluate fitness
				double fitness = this.evaluateFitness(mutant, playerProfile);
				mutant.setFitness(fitness);
				// Add mutant to new population
				newPopulation.add(mutant);
				// Create a list of parents and remember it in a hash
				ArrayList<MyDNA> p = new ArrayList<MyDNA>();
				p.add(parent);
				parents.put(mutant, p);
			}
			
			
			// Do Crossovers
			for (int i=0; i < this.numberOfCrossovers(); i++) {
				// Pick two parents
				MyDNA parent1 = this.pickIndividualForCrossover(newPopulation, null);
				MyDNA parent2 = this.pickIndividualForCrossover(newPopulation, parent1);
				
				if (parent1 != null && parent2 != null) {
					// Crossover produces one or more children
					ArrayList<MyDNA> children = parent1.crossover(parent2);
					
					// Add children to new population and remember their parents
					for (int j=0; j < children.size(); j++) {
						// Get a child
						MyDNA child = children.get(j);
						// Evaluate fitness
						double fitness = this.evaluateFitness(child, playerProfile);
						child.setFitness(fitness);
						// Add it to new population
						newPopulation.add(child);
						// Create a list of parents and remember it in a hash
						ArrayList<MyDNA> p = new ArrayList<MyDNA>();
						p.add(parent1);
						p.add(parent2);
						parents.put(child, p);
					}
				}
				
			}
			
			// Cull the population
			// There is more than one way to do it.
			if (this.competeWithParentsOnly()) {
				population = this.competeWithParents(population, newPopulation, parents);
			}
			else {
				population = this.globalCompetition(population, newPopulation);
			}
			
			//increment counter
			count = count + 1;

			if (this.verbose) {
				MyDNA best = this.getBestIndividual(population);
				System.out.println("" + count + ": Best: " + best + " fitness: " + best.getFitness());
			}
		}
		
		// Get the winner
		solution = this.getBestIndividual(population);
		
		if (this.verbose) {
			System.out.println("Solution: " + solution + " fitnes: " + solution.getFitness());
		}
		
		return solution;
	}
	
	// Create a random individual.
	private MyDNA generateRandomIndividual ()
	{
		MyDNA individual = new MyDNA();
		// YOUR CODE GOES BELOW HERE

		// Build DNA like C2E2S5...but not sure how this works, so rebuild...
		// individual.setChromosome("C2E2S5");
		// ArrayList<Integer> listOfRandom = new ArrayList<Integer>();
		// Random rand = new Random();
		// for(int i = 0; i<10; i++){
		// 	int randomNum = rand.nextInt(9);
		// 	listOfRandom.add(randomNum);
		// }
		// StringBuilder sb = new StringBuilder();
		// int index = 0;
		// sb.append('C');
		// int currentRandNum= listOfRandom.get(index++);
		// sb.append(currentRandNum);
		// sb.append('E');
		// sb.append(listOfRandom.get(index++));
		// sb.append('S');
		// sb.append(listOfRandom.get(index++));
		// sb.append('J');
		// sb.append(listOfRandom.get(index++));
		// individual.setChromosome(sb.toString());

		// Build DNA with length of 50
		int length_dna = 50;
		StringBuilder sb = new StringBuilder();
		Random rand = new Random();
		for (int i = 0; i<length_dna; i++){
			int randomNum = rand.nextInt(4);
			sb.append(randomNum);
		}
		individual.setChromosome(sb.toString());
		// testing Jump
		// individual.setChromosome("111111111111111111");
		// YOUR CODE GOES ABOVE HERE
		return individual;
	}
	
	// Returns true if the genetic algorithm should .
	private boolean terminate (ArrayList<MyDNA> population, int count)
	{
		boolean decision = false;
		// YOUR CODE GOES BELOW HERE
		// if(population.size()>count){
		// 	decision = true;
		// }
		if(count>50){
			decision = true;
		}
		// YOUR CODE GOES ABOVE HERE
		return decision;
	}
	
	// Return a list of individuals that should be copied and mutated.
	private ArrayList<MyDNA> selectIndividualsForMutation (ArrayList<MyDNA> population)
	{
		// TODO: use fitness to determine
		ArrayList<MyDNA> selected = new ArrayList<MyDNA>();

		// YOUR CODE GOES BELOW HERE
		if(population.size()>3){
			MyDNA[] values = new MyDNA[population.size()];
			// System.out.println ("values: " + values);
			// System.out.println ("population.size(): " + population.size());
			for(int i = 0; i<values.length; i++){
				values[i] = population.get(i);
			}
			MyDNA[] topnValues = findTopNValues(values, population.size()/3);
			if(topnValues!=null){
			// MyDNA testing = population.get(0);
			// for (int i = 0; i<population.size(); i++){
			// 	if(i%2==0){
			// 		MyDNA current = population.get(i);
			// 	}
			// }
				for(int i = 0; i<topnValues.length; i++){
					selected.add(topnValues[i]);
				}
			}
		}
		// YOUR CODE GOES ABOVE HERE
		return selected;
	}
	
	// Returns the size of the population.
	private int getPopulationSize ()
	{
		int num = 1; // Default needs to be changed
		// YOUR CODE GOES BELOW HERE
		// testing
		num = 500;
		// YOUR CODE GOES ABOVE HERE
		return num;
	}
	
	// Returns the number of times crossover should happen per iteration.
	private int numberOfCrossovers ()
	{
		int num = 0; // Default is no crossovers
		// YOUR CODE GOES BELOW HERE
		num = 20;
		// YOUR CODE GOES ABOVE HERE
		return num;

	}
	
	// Pick one of the members of the population that is not the same as excludeMe
	private MyDNA pickIndividualForCrossover (ArrayList<MyDNA> population, MyDNA excludeMe)
	{
		MyDNA picked = null;
		// YOUR CODE GOES BELOW HERE
		Random rand = new Random();
		// picked = population.get(randNum);

		if(population.size()>0){
			int randNum = rand.nextInt(population.size());
			picked = population.get(randNum);
		}else{
			return null;
		}
		// YOUR CODE GOES ABOVE HERE
		if (picked == excludeMe) {
			return null;
		}
		else {
			return picked;
		}
	}
	
	// Returns true if children compete to replace parents.
	// Retursn false if the the global population competes.
	private boolean competeWithParentsOnly ()
	{
		boolean doit = false;
		// YOUR CODE GOES BELOW HERE
		
		// YOUR CODE GOES ABOVE HERE
		return doit;
	}
	
	// Determine if children are fitter than parents and keep the fitter ones.
	private ArrayList<MyDNA> competeWithParents (ArrayList<MyDNA> oldPopulation, ArrayList<MyDNA> newPopulation, Hashtable parents)
	{
		ArrayList<MyDNA> finalPopulation = new ArrayList<MyDNA>();
		// YOUR CODE GOES BELOW HERE
		
		// YOUR CODE GOES ABOVE HERE
		if (finalPopulation.size() != this.getPopulationSize()) {
			System.err.println("Population not the correct size." + finalPopulation.size());
			System.exit(1);
		}
		return finalPopulation;
	}
	
	// Combine the old population and the new population and return the top fittest individuals.
	private ArrayList<MyDNA> globalCompetition (ArrayList<MyDNA> oldPopulation, ArrayList<MyDNA> newPopulation)
	{
		ArrayList<MyDNA> finalPopulation = new ArrayList<MyDNA>();
		// YOUR CODE GOES BELOW HERE
		MyDNA[] values = new MyDNA[oldPopulation.size()+newPopulation.size()];
		int count = 0;
		for(int i = 0; i<oldPopulation.size(); i++){
			values[count] = oldPopulation.get(i);
			count++;
		}
		for(int i = 0; i<newPopulation.size(); i++){
			values[count] = newPopulation.get(i);
			count++;
		}
		MyDNA[] highestDNA = findTopNValues(values,this.getPopulationSize());
		for(int i = 0; i<highestDNA.length; i++){
			finalPopulation.add(highestDNA[i]);
		}
		// System.out.println("oldPopulation size: " + oldPopulation.size());
		// System.out.println("newPopulation size: " + newPopulation.size());
		// for(int i = 0; i<oldPopulation.size(); i++){
		// 	finalPopulation.add(oldPopulation.get(i));
		// }

		// ArrayList<MyDNA> compareDNA = new ArrayList<MyDNA>();
  //     	for (DNA temp : oldPopulation)
  //             compareDNA.add(newPopulation.getFitness    al2.contains(temp) ? "Yes" : "No");
  //         System.out.println(al3);
		// YOUR CODE GOES ABOVE HERE
		if (finalPopulation.size() != this.getPopulationSize()) {
			System.err.println("Population not the correct size." + finalPopulation.size());
			System.exit(1);
		}
		return finalPopulation;
	}
	
	public MyDNA[] findTopNValues(MyDNA[] values, int n) {
	    int length = values.length;
	    for (int i=1; i<length; i++) {
	        int curPos = i;
	        while ((curPos > 0) && (values[i].getFitness() > values[curPos-1].getFitness())) {
	            curPos--;
	        }

	        if (curPos != i) {
	            MyDNA element = values[i];
	            System.arraycopy(values, curPos, values, curPos+1, (i-curPos));
	            values[curPos] = element;
	        }
	    }    
	    return Arrays.copyOf(values, n);        
	}   

	// Return the fittest individual in the population.
	private MyDNA getBestIndividual (ArrayList<MyDNA> population)
	{
		MyDNA best = population.get(0);
		double bestFitness = Double.NEGATIVE_INFINITY;
		for (int i=0; i < population.size(); i++) {
			MyDNA current = population.get(i);
			double currentFitness = current.getFitness();
			if (currentFitness > bestFitness) {
				best = current;
				bestFitness = currentFitness;
			}
		}
		return best;
	}
	
	// Changing this function is optional.
	private double evaluateFitness (MyDNA dna, PlayerProfile playerProfile)
	{
		double fitness = 0.0;
		// YOUR CODE GOES BELOW HERE
		MyLevel level = new MyLevel(dna, LevelInterface.TYPE_OVERGROUND);
		fitness = playerProfile.evaluateLevel(level);
		// YOUR CODE GOES ABOVE HERE
		return fitness;
	}
	
	private MyDNA postProcess (MyDNA dna)
	{
		// YOUR CODE GOES BELOW HERE
		
		// YOUR CODE GOES ABOVE HERE
		return dna;
	}
	
	//for this to work, you must implement MyDNA.toString()
	private void printPopulation (ArrayList<MyDNA> population)
	{
		for (int i=0; i < population.size(); i++) {
			MyDNA dna = population.get(i);
			System.out.println("Individual " + i + ": " + dna + " fitness: " + dna.getFitness());
		}
	}
	
	// MAKE ANY NEW MEMBER FUNCTIONS HERE
	
}
