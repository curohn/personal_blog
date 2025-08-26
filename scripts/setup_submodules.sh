#!/bin/bash
# Script to add project repositories as submodules

# Add each project repo as a submodule
git submodule add https://github.com/curohn/delivery_app_simulation.git submodules/delivery_app_simulation
git submodule add https://github.com/curohn/wage_distribution.git submodules/wage_distribution  
git submodule add https://github.com/curohn/global_temperatures.git submodules/global_temperatures

# Create symlinks from submodule READMEs to projects folder
ln -sf ../submodules/delivery_app_simulation/README.md projects/delivery_app_simulation.md
ln -sf ../submodules/wage_distribution/README.md projects/wage_distribution.md
ln -sf ../submodules/global_temperatures/README.md projects/global_temperature_analysis.md

echo "Submodules added! Run 'git submodule update --remote' to update them."
