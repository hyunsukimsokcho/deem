# Deem

Here's the entire components of MLclean for DEEM 2019. If one wants to test each component independently, one absolutely can by following the instructions below:
###### Note: Roughly implemented Duplicator component. (Mar. 02, 2019)
###### Note: Test available for Duplicator and Cleaner component. (Mar. 10, 2019)
First of all, `git clone` this project to wherever you want to in your local machine. This project doesn't require you to pre-install any Python libraries.

Once you're done with cloning, on the root of the project(`${path_you_cloned}/deem`), enter the following:
`python Component/${component_name}.py`. We tried to modularize each components so that the execution of each component with diffrent dataset becomes very handy.
Beacause of the dependencies in execution order, execution of the entire pipeline may only be available in *DEEM.ipynb* notebook file.

