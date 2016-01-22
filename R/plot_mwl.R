get_col_vec <- function(x) {
    ttl_lilac <- rgb(160/255, 40/255, 140/255)

    cv <-  rep("white", length(x))
    ind <- (x > 0)
    cv[ind] <- ttl_lilac
    cv
}

read_data <- function(f) {
    read.csv(f, sep = ",", header = FALSE, col.names = c("time", "bb", "hr","mwl"))
}


fname <- "../python/example_1/mwl.csv"
data      <- read_data(fname)

cv <- get_col_vec(data$mwl)

## define colours
ttl_blue <- rgb(0/255, 60/255, 120/255)
ttl_lilac <- rgb(160/255, 40/255, 140/255)

## PDF
pdf("/tmp/Fig5.pdf", width = 5.2, height = 4, pointsize = 3)
par(mfrow = c(2, 1))
plot(data$time, data$bb, type = "l", col = ttl_blue, xlab = "Time [seconds]", ylab = "Brainbeat [arbitrary units]", ylim = c(0, 6), xlim = c(0, 300))
points(data$time, data$bb, col = ttl_blue, pch = 21, bg = cv, cex = 1.5)

plot(data$time, data$hr, type = "l", col = ttl_blue, xlab = "Time [seconds]", ylab = "Average heart rate [bpm]", ylim = c(55, 75), xlim = c(0, 300))
points(data$time, data$hr, col = ttl_blue, pch = 21, bg = cv, cex = 1.5)
dev.off()

## EPS
postscript("/tmp/Fig5.eps", width = 5.2, height = 4, pointsize = 3, horizontal = FALSE, onefile = FALSE, paper = "special")
par(mfrow = c(2, 1))
plot(data$time, data$bb, type = "l", col = ttl_blue, xlab = "Time [seconds]", ylab = "Brainbeat [arbitrary units]", ylim = c(0, 6), xlim = c(0, 300))
points(data$time, data$bb, col = ttl_blue, pch = 21, bg = cv, cex = 1.5)

plot(data$time, data$hr, type = "b", col = ttl_blue, xlab = "Time [seconds]", ylab = "Average heart rate [bpm]", ylim = c(55, 75), xlim = c(0, 300))
points(data$time, data$hr, col = ttl_blue, pch = 21, bg = cv, cex = 1.5)
dev.off()
