package dk.itu.mario.engine.level;

import java.util.Random;
import java.util.*;

//Make any new member variables and functions you deem necessary.
//Make new constructors if necessary
//You must implement mutate() and crossover()

//Yuen Han Chan
public class MyDNA extends DNA
{
	
	public int numGenes = 0; //number of genes

	// Return a new DNA that differs from this one in a small way.
	// Do not change this DNA by side effect; copy it, change the copy, and return the copy.
	public MyDNA mutate ()
	{
		MyDNA copy = new MyDNA();
		System.out.println ("DNA: " + getChromosome());
		//YOUR CODE GOES BELOW HERE
		String currentDNA = getChromosome();
		// StringBuilder mutateDNA = new StringBuilder();
		Random rand = new Random();
		int indexToChange = rand.nextInt(currentDNA.length());
		int changeOccur = rand.nextInt(4); // only change it from 0-3
		String mutateDNA_string = currentDNA.substring(0,indexToChange) + changeOccur + currentDNA.substring(indexToChange+1,currentDNA.length());
		copy.setChromosome(mutateDNA_string);

		// for(int i = 0; i<currentDNA.length(); i++){
		// 	char curr = currentDNA.charAt(i);
		// 	boolean isDigit = (curr >= '0' && curr <= '9');
		// 	if(isDigit){
		// 		if(curr!=9){
		// 			curr+=1;
		// 		}
		// 	}
		// 	mutateDNA.append(curr);
		// }
		// copy.setChromosome(mutateDNA.toString());
		//YOUR CODE GOES ABOVE HERE
		System.out.println ("DNA_mutate: " + copy.getChromosome());
		return copy;
	}
	
	// Do not change this DNA by side effect
	public ArrayList<MyDNA> crossover (MyDNA mate)
	{
		ArrayList<MyDNA> offspring = new ArrayList<MyDNA>();
		//YOUR CODE GOES BELOW HERE
		String origDNA_1 = getChromosome();
		String origDNA_2 = mate.getChromosome();
		if (origDNA_1.length() !=origDNA_2.length()){
			System.out.println("BAD: two DNA to combine are not same length!");
			System.out.println("1st DNA: " + origDNA_1);
			System.out.println("2nd DNA: " + origDNA_2);
		}
		else{
			int splitPoint = origDNA_1.length()/2;
			String newDNA_1 = origDNA_1.substring(0,splitPoint) + origDNA_2.substring(splitPoint);
			String newDNA_2 = origDNA_2.substring(0,splitPoint) + origDNA_1.substring(splitPoint);

			// for debugging
			System.out.println("1st DNA_crossover: " + newDNA_1);
			System.out.println("2nd DNA_crossover: " + newDNA_2);
			// end debuggin

			MyDNA myDNA_1 = new MyDNA();
			MyDNA myDNA_2 = new MyDNA();
			myDNA_1.setChromosome(newDNA_1);
			myDNA_2.setChromosome(newDNA_2);
			offspring.add(myDNA_1);
			offspring.add(myDNA_2);
		}
		//YOUR CODE GOES ABOVE HERE
		return offspring;
	}
	
	// Optional, modify this function if you use a means of calculating fitness other than using the fitness member variable.
	// Return 0 if this object has the same fitness as other.
	// Return -1 if this object has lower fitness than other.
	// Return +1 if this objet has greater fitness than other.
	public int compareTo(MyDNA other)
	{
		int result = super.compareTo(other);
		//YOUR CODE GOES BELOW HERE
		
		//YOUR CODE GOES ABOVE HERE
		return result;
	}
	
	
	// For debugging purposes (optional)
	public String toString ()
	{
		String s = super.toString();
		//YOUR CODE GOES BELOW HERE
		
		//YOUR CODE GOES ABOVE HERE
		return s;
	}
	
	public void setNumGenes (int n)
	{
		this.numGenes = n;
	}

}

