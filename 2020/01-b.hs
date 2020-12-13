main = do
  d <- readFile "input/01.input"
  let numbers = map read (words d)
  let pairs = [x * y * z | x <- numbers, y <- numbers, z <- numbers, x < y, y < z, x + y + z == 2020]
  print pairs
