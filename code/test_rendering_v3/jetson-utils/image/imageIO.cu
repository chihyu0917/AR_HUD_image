#include "imageIO.h"
#include "cudaUtility.h"

template<typename T>
__global__ void gpuDetectionOverlayBox_pat( T* input, T* output, int imgWidth, int imgHeight, T* pattern, int x0, int y0, int boxWidth, int boxHeight, const float pat_alpha ) 
{
	const int box_x = blockIdx.x * blockDim.x + threadIdx.x;
	const int box_y = blockIdx.y * blockDim.y + threadIdx.y;

	if( box_x >= boxWidth || box_y >= boxHeight )
		return;

	const int x = box_x + x0;
	const int y = box_y + y0;

	if( x >= imgWidth || y >= imgHeight )
		return;

	const T px_in = pattern[ box_y * boxWidth + box_x ];
	if( px_in.w !=0 )
	{
		if( pat_alpha == 0)
		{
			const T img_in = input[ y * imgWidth + x ];
			output[y * imgWidth + x] = img_in;
		}
		else if( pat_alpha == 255)
			output[y * imgWidth + x] = px_in;
		else
		{
			const float alpha = pat_alpha / 255.0f;
			const float ialph = 1.0f - alpha;
			const T img_in = input[ y * imgWidth + x ];
			output[y * imgWidth + x] = make_float4( alpha * px_in.x + ialph * img_in.x, 
					alpha * px_in.y + ialph * img_in.y,
					alpha * px_in.z + ialph * img_in.z,
					img_in.w );
		}
	}
}

cudaError_t cudaDetectionOverlay_pat( float4* input, float4* output, uint32_t width, uint32_t height, float4* pattern, uint32_t x0, uint32_t y0, uint32_t pat_width, uint32_t pat_height, const float alpha)
{
	if( !input || !output || input != output || width == 0 || height == 0 || !pattern || pat_width == 0 || pat_height == 0 )
		return cudaErrorInvalidValue;

	const int boxWidth = (int)pat_width;
	const int boxHeight = (int)pat_height;

			// launch kernel
	const dim3 blockDim(8, 8);
	const dim3 gridDim(iDivUp(boxWidth,blockDim.x), iDivUp(boxHeight,blockDim.y));
	gpuDetectionOverlayBox_pat<float4><<<gridDim, blockDim>>>(input, output, width, height, pattern, x0, y0, boxWidth, boxHeight, alpha);
	return cudaGetLastError(); 
}

template<typename T>
__global__ void gpuDetectionOverlay_pat_selfalpha( T* input, T* output, int imgWidth, int imgHeight, T* pattern, int x0, int y0, int boxWidth, int boxHeight ) 
{
	const int box_x = blockIdx.x * blockDim.x + threadIdx.x;
	const int box_y = blockIdx.y * blockDim.y + threadIdx.y;

	if( box_x >= boxWidth || box_y >= boxHeight )
		return;

	const int x = box_x + x0;
	const int y = box_y + y0;

	if( x >= imgWidth || y >= imgHeight )
		return;

	const T px_in = pattern[ box_y * boxWidth + box_x ];
	if( px_in.w !=0 )
	{

		if( px_in.w == 255)
			output[y * imgWidth + x] = px_in;
		else
		{
			const float alpha = px_in.w / 255.0f;
			const float ialph = 1.0f - alpha;
			const T img_in = input[ y * imgWidth + x ];
			output[y * imgWidth + x] = make_float4( alpha * px_in.x + ialph * img_in.x, 
					alpha * px_in.y + ialph * img_in.y,
					alpha * px_in.z + ialph * img_in.z,
					img_in.w );
		}
	}
}

cudaError_t cudaDetectionOverlay_pat_selfalpha( float4* input, float4* output, uint32_t width, uint32_t height, float4* pattern, uint32_t x0, uint32_t y0, uint32_t pat_width, uint32_t pat_height)
{
	if( !input || !output || input != output || width == 0 || height == 0 || !pattern || pat_width == 0 || pat_height == 0 )
		return cudaErrorInvalidValue;

	const int boxWidth = (int)pat_width;
	const int boxHeight = (int)pat_height;

			// launch kernel
	const dim3 blockDim(8, 8);
	const dim3 gridDim(iDivUp(boxWidth,blockDim.x), iDivUp(boxHeight,blockDim.y));
	gpuDetectionOverlay_pat_selfalpha<float4><<<gridDim, blockDim>>>(input, output, width, height, pattern, x0, y0, boxWidth, boxHeight);
	return cudaGetLastError(); 
}

template<typename T>
__global__ void gpuDetectionOverlay_all( T* input, T* output, int imgWidth, int imgHeight, const float4 color ) 
{
	const int x = blockIdx.x * blockDim.x + threadIdx.x;
	const int y = blockIdx.y * blockDim.y + threadIdx.y;

	if( x >= imgWidth || y >= imgHeight )
		return;

	const T px_in = input[ y * imgWidth + x ];



	if( color.w == 255)
		output[y * imgWidth + x] = color;
	else
	{
		const float alpha = color.w / 255.0f;
		const float ialph = 1.0f - alpha;
		output[y * imgWidth + x] = make_float4( alpha * color.x + ialph * px_in.x, 
					alpha * color.y + ialph * px_in.y,
					alpha * color.z + ialph * px_in.z,
					px_in.w );
	}
}

cudaError_t cudaDetectionOverlay_all( float4* input, float4* output, uint32_t width, uint32_t height, const float4 color)
{
	if( !input || !output || input != output || width == 0 || height == 0 )
		return cudaErrorInvalidValue;

			// launch kernel
	const dim3 blockDim(8, 8);
	const dim3 gridDim(iDivUp(width,blockDim.x), iDivUp(height,blockDim.y));
	gpuDetectionOverlay_all<float4><<<gridDim, blockDim>>>(input, output, width, height, color);
	return cudaGetLastError(); 
}
