filename <- 'signal_50MHz.bin'
zz <- file(filename, "rb")

BajtowNaLiczbe = 4
fsize = file.size(filename)
LiczbaLiczb = fsize / BajtowNaLiczbe
v<-readBin(zz, numeric(), size=BajtowNaLiczbe, endian="little", n=LiczbaLiczb)
close(zz)

# Ustawienie progu detekcji impulsów na 0.9998 kwantyla
threshold = quantile(v, 0.99985)
print(threshold)
print(v[1:10])
plot(v[1:100000], type='l', xlab="Indeks", ylab="Natężenie")     # dłuższy fragment
idx = 67650:67900;
plot(idx, v[idx],type='l', xlab="Indeks", ylab="Natężenie")# jeden impuls - aby zobaczyć kształt impulsów

# Zadanie 2

print(threshold)

# Znajdź indeksy, gdzie sygnał przekracza próg (indeksy impulsów)
impulse_indices <- which(v > threshold)

# Znajdź indeksy, gdzie sygnał nie przekracza progu (indeksy nie-impulsów)
non_impulse_indices <- setdiff(1:length(v), impulse_indices)

# Wykres części sygnału z zaznaczonymi impulsami
idx_max = length(v)/20
v_part = v[0 : idx_max]
impulse_indices_part = impulse_indices[impulse_indices <= idx_max]
plot(v_part, type = 'l', main = "Sygnał z wykrytymi impulsami", xlab="Indeks", ylab="Natężenie")
points(impulse_indices_part, v[impulse_indices_part], col = 'blue', pch = 16)

idx = 67650:67900;
plot(idx, v[idx],type='l', xlab="Indeks", ylab="Natężenie")# jeden impuls - aby zobaczyć kształt impulsów
impulse_indices2 = impulse_indices[impulse_indices >= 67650]
impulse_indices2 = impulse_indices2[impulse_indices2 <= 67900]
points(impulse_indices2, v[impulse_indices2], col = 'blue', pch = 16)

#a)
# Analiza fragmentu sygnału bez impulsów
non_impulse_signal <- v[non_impulse_indices]

# Wykres histogramu
hist(non_impulse_signal, main="Histogram Sygnału bez Impulsów", xlab="Natężenie", ylab="Liczebność", col="lightblue")
boxplot(non_impulse_signal, main="Wykres pudełkowy Sygnału bez Impulsów", xlab="Natężenie", ylab="Liczebność", col="lightblue")

#b)Badanie rozkładu odstępów czasu między impulsami

# Znajdź odstępy czasu między impulsami
ilosc_probek_miedzy_impulsami <- diff(impulse_indices)

# Wybierz tylko te odstępy czasu, które są wystarczająco długie
time_gaps <- ilosc_probek_miedzy_impulsami[ilosc_probek_miedzy_impulsami > 200]
print(time_gaps)


# Sprawdź, czy time_gaps nie jest puste
if (length(time_gaps) > 0) {
  num_breaks <- 30

  # Wykres histogramu odstępów czasu
  time_gaps = time_gaps  / 50e6 * 1000 # w ms
  hist(time_gaps, breaks = num_breaks, main = "Histogram Odstępów Czasu Między Impulsami", xlab = "Odstęp czasu [ms]", ylab = "Liczebność", col = "lightgreen")
} else {
  cat("Brak danych do wygenerowania histogramu.\n")
}

