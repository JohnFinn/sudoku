trait Sudoku{
    fn get(&self, x: i8, y: i8) -> i8;
    fn set(&self, x: i8, y: i8, value: i8);
    fn row(&self, row: i8) -> Iterator<Item=&mut i8>;
    fn column(&self, column: i8) -> Iterator<Item=&mut i8>;
    fn block(&self, x: i8, y: i8) -> Iterator<Item=&mut i8>;
    fn solve(&self);
}
