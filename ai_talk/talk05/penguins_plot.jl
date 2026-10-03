using Pkg
Pkg.add("PalmerPenguins")
using PalmerPenguins

Pkg.add(["DataFrames", "AlgebraOfGraphics", "CairoMakie"])
using DataFrames
using AlgebraOfGraphics, CairoMakie

ENV["DATADEPS_ALWAYS_ACCEPT"] = "true"

penguins_julia = DataFrame(PalmerPenguins.load())
dropmissing!(
  penguins_julia,
  [:flipper_length_mm, :body_mass_g, :species]
)

plot = data(penguins_julia) *
  mapping(
    :flipper_length_mm,
    :body_mass_g,
    color = :species
  ) *
  (visual(Scatter) + linear())

figure = draw(plot; axis = (
  title = "Penguin Body Mass and Flipper Length in Julia",
  xlabel = "Flipper length (mm)",
  ylabel = "Body mass (g)"
))

output_dir = joinpath(@__DIR__, "images")
mkpath(output_dir)
save(joinpath(output_dir, "julia_penguins.png"), figure)
