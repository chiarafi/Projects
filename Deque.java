//////////////////////////
//Submission by:
//
//Chiara Fischer
//
//////////////////////////

public class Deque {	
	private int[] data;       // array storing the data
	private int left;         // index to the left end of the deque
	private int right;        // index to the right end of the deque
	private final int size;   // maximal capacity of the deque

	public static void main(String[] args) {
		try {
			// create a deque of size 10
			Deque deque = new Deque(10);
			
			// enqueue elements on the right side
			System.out.println("Enqueue 1,2,3 from the right");
			deque.enqueueRight(1);
			deque.enqueueRight(2);
			deque.enqueueRight(3);
//deque.enqueueRight(4);
			System.out.println("Expected: [1 2 3]");
			System.out.print("Actual:   ");
			deque.printElements();
			
			// enqueue elements on the left side
			System.out.println("Enqueue 4,5,6 from the left");
			deque.enqueueLeft(4);
			deque.enqueueLeft(5);
			deque.enqueueLeft(6);
			System.out.println("Expected: [6 5 4 1 2 3]");
			System.out.print("Actual:   ");
			deque.printElements();
			
			// deque elements from the right side
			System.out.println("Dequeue twice from the right");
			deque.dequeueRight();
			deque.dequeueRight();
			System.out.println("Expected: [4 1 2 3]");
			System.out.print("Actual:   ");
			deque.printElements();
			
			// deque elements from the left side
			System.out.println("Dequeue once from the left");
			deque.dequeueLeft();
			System.out.println("Expected: [4 1 2]");
			System.out.print("Actual:   ");
			deque.printElements();
		
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	// constructor with the maximal number of elements the deque can hold
	public Deque (int size) {
		data       = new int[size];
		left       = 1;     // indices are 1-based
		right      = 1;		// indices are 1-based
		this.size  = size;
	}

	// Hilfsfunktion, die die bereits eingefügten Elemente in Array zählt
	public int getSize(int[] data) { 
		int n=0;
		for(int i=0; i<size; i++) {
		 if(data[i]!=0) {
			n++;
	
		}}
		return n;
	}
	

	
	//////////////////////
	// Task 8.3
	// Implement enqueueLeft that adds a new element on the left side of the
	// deque or throws an exception if the deque is full, you can use 
    // throw new Exception("some error message");
	public void enqueueLeft(int x) throws Exception{
		if(getSize(data)==size) {throw new Exception();} // falls voll
		if(left==1) { // falls bis nach vorne aufgefüllt: Verschiebung notwendig 
			
			for(int i=right-1;i>=1;i--) { // Verschiebungen nach rechts 
				data[i] = data[i-1];
			}
			right++; // Index des rechten Elementes erhöht 
			data[0] = x; // vorne (links) einfügen 
		}
		else {
		left--;
		data[left-1] = x; }
		
		
	}
	
	//////////////////////
	// Task 8.3
	// Implement enqueueRight that adds a new element on the right side of the
	// deque or throws an exception if the deque is full, you can use 
    // throw new Exception("some error message");

	
	public void enqueueRight (int x) throws Exception {
		if(getSize(data)==size) {throw new Exception();} // voll

		if(right==size) { //rechts aufgefüllt also verschiebung notwenig
			right=1; data[size-1] =x;
			} else {
				right++; data[right-2]=x; }
	}



	//////////////////////
	// Task 8.3
	// Implement dequeueLeft that removes the right-most element from the deque
	// and returns this element or throws an exception if the deque is empty, 
    // you can use 
    // throw new Exception("some error message");
	public int dequeueRight() throws Exception {
		if(getSize(data)==0) {throw new Exception();} // falls leer 
		int x=data[left-1]; // Element ganz rechts merken
		data[left-1] = 0; // Element überschreiben mit 0 
		left++; // Index des Elementes, das am weitesten links liegt um 1 erhöhen 
		
		return x; // Element zurückgeben
	}

	//////////////////////
	// Task 8.3
	// Implement dequeueRight that removes the left-most element from the deque
	// and returns this element or throws an exception if the deque is empty, 
    // you can use 
    // throw new Exception("some error message");
	public int dequeueLeft() throws Exception {
		if(getSize(data)==0) {throw new Exception();} // falls leer
		int x=data[right-1]; // Element merken
		data[right-1] = 0; // überschreiben mit 0, d.h. löschen
		right--;
		
		return x;}
	
	// prints all elements starting from left to right
	public void printElements() {
		String msg = "[";
		
		// get the left most element
		if(left != right)
			msg += data[left-1];
		
		// start iteration with the second element since we already got the value
		// of the first element, make sure to wrap around the array when left
		// is at the end of the underlying array
		int cur = (left == size) ? 1 : left+1;
		
		// retrieve all elements until we reach the right end
		while(cur != right) {	
			msg += " " + data[cur-1];
			cur++;
			if(cur > size)
				cur = 1;
		}
		msg += "]";
		System.out.println(msg);
	}
}
