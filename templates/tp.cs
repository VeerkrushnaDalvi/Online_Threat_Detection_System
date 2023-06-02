public class Customer{
    public int Id {get; set;}
    public string Name {get; set;}

    public string City {get; set;}

    public ovveride string ToString(){
        return Id +" " + Name + " "
    }
}