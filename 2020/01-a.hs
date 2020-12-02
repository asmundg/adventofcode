main = do
  d <- readFile "input/01.input"
  let numbers = map read (words d)
  let pairs = [x * y | x <- numbers, y <- numbers, x < y, x + y == 2020]
  print pairs
